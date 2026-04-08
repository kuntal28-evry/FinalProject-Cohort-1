import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.test_analyst import test_analyst_agent
from agents.risk_scorer import risk_scorer_agent
from agents.rca_agent import rca_agent
from agents.comms_agent import comms_agent

def read_file(path):
    with open(path, "r") as f:
        return f.read()

async def call_agent(agent, session_service, session_id, prompt):
    await session_service.create_session(app_name="qualityguard", user_id="qa-engineer", session_id=session_id)
    runner = Runner(agent=agent, app_name="qualityguard", session_service=session_service)
    final_response = ""
    async for event in runner.run_async(
        user_id="qa-engineer",
        session_id=session_id,
        new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
    return final_response

async def run_qualityguard():
    print("\n" + "="*60)
    print("   QualityGuard AI — Release Intelligence System")
    print("="*60)
    test_report = read_file("data/sample_test_report.xml")
    build_log = read_file("data/sample_build_log.txt")
    session_service = InMemorySessionService()

    print("\n🔍 STEP 1: Test Analyst Agent analyzing test report...\n")
    analysis = await call_agent(test_analyst_agent, session_service, "s1", f"Analyze this JUnit XML test report:\n\n{test_report}")
    print(analysis)

    print("\n" + "─"*60)
    print("\n⚠️  STEP 2: Risk Scorer calculating release risk...\n")
    risk = await call_agent(risk_scorer_agent, session_service, "s2", f"Calculate release risk score from this test analysis:\n\n{analysis}")
    print(risk)

    print("\n" + "─"*60)
    print("\n🔎 STEP 3: RCA Agent performing root cause analysis...\n")
    rca = await call_agent(rca_agent, session_service, "s3", f"Build logs:\n{build_log}\n\nTest failures:\n{analysis}")
    print(rca)

    print("\n" + "─"*60)
    print("\n📧 STEP 4: Comms Agent drafting stakeholder email...\n")
    email = await call_agent(comms_agent, session_service, "s4", f"TEST ANALYSIS:\n{analysis}\n\nRISK SCORE:\n{risk}\n\nROOT CAUSE:\n{rca}")
    print(email)

    print("\n" + "="*60)
    print("   QUALITYGUARD AI ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_qualityguard())
