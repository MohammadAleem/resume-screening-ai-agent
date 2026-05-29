# Basic tests for Resume Screening AI Agent

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_python_version():
    """Ensure Python 3.8 or higher is being used"""
    assert sys.version_info >= (3, 8), "Python 3.8+ required"

def test_required_packages():
    """Ensure all required packages are importable"""
    try:
        import flask
        assert True
    except ImportError:
        assert False, "Flask is not installed"

def test_environment_structure():
    """Ensure project structure is correct"""
    assert os.path.exists("requirements.txt"), "requirements.txt missing"
    assert os.path.exists(".gitignore"), ".gitignore missing"
    assert os.path.exists("Dockerfile"), "Dockerfile missing"

def test_placeholder():
    """Placeholder test — replace with real app logic tests"""
    result = 2 + 2
    assert result == 4
