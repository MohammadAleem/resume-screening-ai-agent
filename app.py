import os
import json
import time
import serial
import fitz  # PyMuPDF
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Arduino Connection ──────────────────────────────
ARDUINO_PORT = "COM3"
try:
    arduino_serial = serial.Serial(ARDUINO_PORT, 9600, timeout=2)
    time.sleep(2)
    print(f"✅ Arduino connected on {ARDUINO_PORT}")
except Exception as e:
    arduino_serial = None
    print(f"⚠️ Arduino not connected: {e}")

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def screen_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert HR resume screener. Analyze the resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Respond ONLY with a valid JSON object in this exact format:
{{
  "decision": "SELECTED" or "REJECTED",
  "score": <number from 0 to 100>,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "summary": "2-3 sentence explanation of your decision"
}}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screen', methods=['POST'])
def screen():
    try:
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({"error": "Job description is required."}), 400

        if 'resume' not in request.files:
            return jsonify({"error": "No resume file uploaded."}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No file selected."}), 400
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are accepted."}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        resume_text = extract_text_from_pdf(file_path)

        if not resume_text:
            return jsonify({"error": "Could not extract text from PDF."}), 400

        result = screen_resume(resume_text, job_description)

        # ── Send signal to Arduino ──────────────────
        signal = 'S' if result['decision'] == 'SELECTED' else 'R'
        if arduino_serial:
            arduino_serial.write(signal.encode())
            print(f"📡 Signal sent to Arduino: {signal}")
        else:
            print(f"⚠️ Arduino not connected. Signal would be: {signal}")

        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "AI returned unexpected response. Try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)