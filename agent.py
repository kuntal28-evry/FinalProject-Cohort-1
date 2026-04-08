import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL", "gemini-1.5-flash")

# -------------------------------
# TOOL: Save user input to state
# -------------------------------
def add_input_to_state(tool_context: ToolContext, prompt: str) -> dict:
    tool_context.state["INPUT"] = prompt
    logging.info(f"[STATE] Saved INPUT")
    return {"status": "ok"}

# -------------------------------
# 1. Test Analyst Agent
# -------------------------------
test_analyst_agent = Agent(
    name="test_analyst",
    model=model_name,
    instruction="""
Analyze the JUnit XML test report.

INPUT:
{ INPUT }

OUTPUT:
## Test Analysis Report
- Total Tests:
- Passed:
- Failed:

## Genuine Failures
...

## Flaky Tests
...

## QA Verdict
...
""",
    output_key="test_analysis"
)

# -------------------------------
# 2. Risk Scorer
# -------------------------------
risk_scorer_agent = Agent(
    name="risk_scorer",
    model=model_name,
    instruction="""
Given the test analysis below, calculate risk score.

TEST ANALYSIS:
{ test_analysis }

OUTPUT:
## Release Risk Score
Score: XX/100
...
""",
    output_key="risk_score"
)

# -------------------------------
# 3. RCA Agent
# -------------------------------
rca_agent = Agent(
    name="rca_agent",
    model=model_name,
    instruction="""
Analyze failures and logs.

TEST ANALYSIS:
{ test_analysis }

OUTPUT:
## Root Cause Analysis
...
""",
    output_key="rca_report"
)

# -------------------------------
# 4. Comms Agent
# -------------------------------
comms_agent = Agent(
    name="comms_agent",
    model=model_name,
    instruction="""
Write stakeholder email.

TEST ANALYSIS:
{ test_analysis }

RISK:
{ risk_score }

RCA:
{ rca_report }

OUTPUT:
## Email Subject
...

## Email Body
...
"""
)

# -------------------------------
# SEQUENTIAL WORKFLOW
# -------------------------------
qualityguard_workflow = SequentialAgent(
    name="qualityguard_workflow",
    description="Runs full release analysis",
    sub_agents=[
        test_analyst_agent,
        risk_scorer_agent,
        rca_agent,
        comms_agent
    ]
)

# -------------------------------
# ROOT AGENT (Manager)
# -------------------------------
root_agent = Agent(
    name="qualityguard_manager",
    model=model_name,
    instruction="""
- Ask user for test report input
- Use tool to save it
- Then run qualityguard_workflow
""",
    tools=[add_input_to_state],
    sub_agents=[qualityguard_workflow]
)