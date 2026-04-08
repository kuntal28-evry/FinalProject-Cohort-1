# QualityGuard AI - Release Intelligence System

An intelligent, multi-agent AI system that automates software release quality analysis, risk assessment, root cause analysis, and stakeholder communication.

## 🎯 Overview

QualityGuard AI is a sophisticated release intelligence system that leverages Google's Agent Development Kit (ADK) to orchestrate multiple specialized AI agents. It analyzes test reports and build logs to provide comprehensive release insights, risk scores, and actionable recommendations.

## 🏗️ Architecture

The system uses a **Sequential Agent Workflow** with four specialized agents:



### Agent Roles

1. **Test Analyst Agent** - Analyzes JUnit XML test reports
   - Identifies genuine failures vs. flaky tests
   - Provides QA verdict and test summary

2. **Risk Scorer Agent** - Calculates release risk score
   - Evaluates test failures impact
   - Provides risk assessment (0-100 scale)

3. **RCA Agent** - Performs root cause analysis
   - Correlates test failures with build logs
   - Identifies underlying issues

4. **Comms Agent** - Drafts stakeholder communication
   - Creates professional email summaries
   - Includes risk scores and recommendations

## 📋 Prerequisites

- Python 3.9+
- Google Cloud Platform account
- Gemini API access (or other supported models)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kuntal28-evry/FinalProject-Cohort-1.git
cd FinalProject-Cohort-1

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate


pip install -r requirements.txt

MODEL=gemini-1.5-flash
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Authenticate with Google Cloud
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

FinalProject-Cohort-1/
├── agents/
│   ├── __init__.py
│   ├──agent.py
├── data/
│   ├── sample_test_report.xml
│   └── sample_build_log.txt
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/5d149db8-a49a-4ac1-998d-5823d5460e1a" />
