![CI Pipeline](https://github.com/MohammadAleem/resume-screening-ai-agent/actions/workflows/ci.yml/badge.svg)
# resume-screening-ai-agent
AI-powered resume screening system using LLaMA 3, Flask, and Arduino
# 🤖 Resume Screening AI Agent

An AI-powered resume screening system that analyzes resumes 
against job descriptions using LLaMA 3, built with Flask backend 
and real-time Arduino hardware feedback.

## 🚀 Features
- Upload PDF resumes and screen them instantly
- AI analyzes resume against job description
- Shows match score, matched skills and missing skills
- Real-time hardware feedback via Arduino (Green/Red LED + Buzzer)

## 🛠️ Tech Stack
- **Python** - Core programming language
- **Flask** - Web framework
- **Groq API** - Free AI API (LLaMA 3 model)
- **PyMuPDF** - PDF text extraction
- **PySerial** - Arduino communication
- **Arduino Uno** - Hardware control

## ⚙️ Hardware
- Arduino Uno
- Green LED (Pin 8) - Candidate Selected
- Red LED (Pin 9) - Candidate Rejected
- Buzzer (Pin 10) - Audio feedback
- 220 ohm resistors

## 📋 How It Works
1. Upload a PDF resume on the web interface
2. Enter the job description
3. AI analyzes and scores the resume
4. Result shown on website with score and skills
5. Arduino LED and Buzzer respond in real time

## 🔧 Installation
1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install libraries: `pip install flask groq pymupdf pyserial python-dotenv`
5. Create `.env` file and add your Groq API key: `GROQ_API_KEY=your_key_here`
6. Run: `python app.py`
7. Open browser: `http://127.0.0.1:5000`

## 📸 Result
- ✅ SELECTED → Green LED ON + Happy Beep
- ❌ REJECTED → Red LED ON + Low Beep


## 👨‍💻 Developer
**Mohammad Aleem**
CSE Engineering Student | Backend + DevOps
🔗 [GitHub](https://github.com/MohammadAleem)
