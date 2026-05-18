# 🛡️ Smart Contract Vulnerability Analyzer (Gemini AI)

## 📌 Overview
This script is an AI-powered tool that automatically analyzes Solidity smart contracts to detect potential security vulnerabilities. It uses the **Gemini AI API** to review smart contract code and identify common blockchain security risks.

The tool helps developers quickly understand weaknesses in their contracts and improves smart contract security during development.

---

## 🚀 Features
- 📂 File selection via GUI (Tkinter)
- 🤖 AI-powered analysis using Gemini API
- 🛡️ Detects 7 major vulnerabilities:
  - Reentrancy
  - Access Control issues
  - Arithmetic issues
  - Unchecked Return Values
  - Denial of Service
  - Front-Running
  - Time Manipulation
- 📊 Structured output for each vulnerability
- 💾 Saves results as JSON file locally
- 🔐 Secure API key handling using `.env`

---

## 🚀 How to Run the Project

1. **Clone the repository:**
```bash
git clone https://github.com/marhum456/smart-contract-ai-analyzer.git
cd smart-contract-ai-analyzer
```

2. **Setup Virtual Environment & Install Dependencies:**
```bash
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```
