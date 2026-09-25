import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

from backend.agents.solution_analyzer import SolutionUnderstandingAgent
from backend.agents.technical_agent import TechnicalFeasibilityAgent
from backend.agents.cost_agent import CostResourceAgent
from backend.agents.privacy_agent import PrivacyRiskAgent
from backend.agents.security_agent import SecurityRiskAgent
from backend.agents.fairness_agent import FairnessRiskAgent
from backend.agents.operational_agent import OperationalReliabilityAgent
from backend.agents.stress_judge import StressJudgeAgent
from backend.agents.report_generator import ReportGeneratorAgent
from backend.workflow import StressTestWorkflow

from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Groq Client
# --------------------------------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in .env file")

client = Groq(api_key=api_key)


# --------------------------------------------------
# AI Agent
# --------------------------------------------------

solution_agent = SolutionUnderstandingAgent(client)
technical_agent = TechnicalFeasibilityAgent(client)
cost_agent = CostResourceAgent(client)
privacy_agent = PrivacyRiskAgent(client)
security_agent = SecurityRiskAgent(client)
fairness_agent = FairnessRiskAgent(client)
operational_agent = OperationalReliabilityAgent(client)
stress_judge = StressJudgeAgent(client)
report_generator = ReportGeneratorAgent(client)

workflow = StressTestWorkflow(client)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class SolutionRequest(BaseModel):
    solution: str


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Stress-AI Backend is running!"
    }


# --------------------------------------------------
# Solution Understanding Endpoint
# --------------------------------------------------

@app.post("/api/analyze-solution")
def analyze_solution(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    analysis = solution_agent.analyze(request.solution)

    return {
        "success": True,
        "analysis": analysis
    }

# --------------------------------------------------
# Technical Analysis Endpoint
# --------------------------------------------------
@app.post("/api/technical-analysis")
def technical_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    understanding = solution_agent.analyze(request.solution)

    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result
    }

# --------------------------------------------------
# Cost Analysis Endpoint
# --------------------------------------------------
@app.post("/api/cost-analysis")
def cost_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    # Step 1: Understand solution
    understanding = solution_agent.analyze(
        request.solution
    )

    # Step 2: Analyze technical feasibility
    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    # Step 3: Analyze cost and resources
    cost_result = cost_agent.analyze(
        request.solution,
        understanding,
        technical_result
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result,
        "cost_analysis": cost_result
    }

# --------------------------------------------------
# Privacy Analysis Endpoint
# --------------------------------------------------

@app.post("/api/privacy-analysis")
def privacy_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    # Step 1: Understand solution
    understanding = solution_agent.analyze(
        request.solution
    )

    # Step 2: Technical analysis
    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    # Step 3: Privacy analysis
    privacy_result = privacy_agent.analyze(
        request.solution,
        understanding,
        technical_result
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result,
        "privacy_analysis": privacy_result
    }
# --------------------------------------------------
# Security Analysis Endpoint
# --------------------------------------------------
@app.post("/api/security-analysis")
def security_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    # 1. Understand the solution
    understanding = solution_agent.analyze(
        request.solution
    )

    # 2. Technical analysis
    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    # 3. Privacy analysis
    privacy_result = privacy_agent.analyze(
        request.solution,
        understanding,
        technical_result
    )

    # 4. Security analysis
    security_result = security_agent.analyze(
        request.solution,
        understanding,
        technical_result,
        privacy_result
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result,
        "privacy_analysis": privacy_result,
        "security_analysis": security_result
    }

# --------------------------------------------------
# Fairness Analysis Endpoint
# --------------------------------------------------
@app.post("/api/fairness-analysis")
def fairness_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    # 1. Understand solution
    understanding = solution_agent.analyze(
        request.solution
    )

    # 2. Technical analysis
    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    # 3. Fairness analysis
    fairness_result = fairness_agent.analyze(
        request.solution,
        understanding,
        technical_result
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result,
        "fairness_analysis": fairness_result
    }

# --------------------------------------------------
# Operational Analysis Endpoint
# --------------------------------------------------
@app.post("/api/operational-analysis")
def operational_analysis(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    # 1. Understand solution
    understanding = solution_agent.analyze(
        request.solution
    )

    # 2. Technical analysis
    technical_result = technical_agent.analyze(
        request.solution,
        understanding
    )

    # 3. Operational analysis
    operational_result = operational_agent.analyze(
        request.solution,
        understanding,
        technical_result
    )

    return {
        "success": True,
        "solution_understanding": understanding,
        "technical_analysis": technical_result,
        "operational_analysis": operational_result
    }

# --------------------------------------------------
# Stress Test Analysis Endpoint
# --------------------------------------------------
@app.post("/api/stress-test")
def stress_test(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    solution = request.solution

    # ------------------------------------------------
    # 1. Solution Understanding
    # ------------------------------------------------

    understanding = solution_agent.analyze(
        solution
    )

    # ------------------------------------------------
    # 2. Technical Analysis
    # ------------------------------------------------

    technical_result = technical_agent.analyze(
        solution,
        understanding
    )

    # ------------------------------------------------
    # 3. Cost Analysis
    # ------------------------------------------------

    cost_result = cost_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ------------------------------------------------
    # 4. Privacy Analysis
    # ------------------------------------------------

    privacy_result = privacy_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ------------------------------------------------
    # 5. Security Analysis
    # ------------------------------------------------

    security_result = security_agent.analyze(
        solution,
        understanding,
        technical_result,
        privacy_result
    )

    # ------------------------------------------------
    # 6. Fairness Analysis
    # ------------------------------------------------

    fairness_result = fairness_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ------------------------------------------------
    # 7. Operational Analysis
    # ------------------------------------------------

    operational_result = operational_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ------------------------------------------------
    # 8. FINAL STRESS JUDGE
    # ------------------------------------------------

    final_result = stress_judge.evaluate(
        solution,
        understanding,
        technical_result,
        cost_result,
        privacy_result,
        security_result,
        fairness_result,
        operational_result
    )

    return {
        "success": True,

        "solution": solution,

        "solution_understanding": understanding,

        "technical_analysis": technical_result,

        "cost_analysis": cost_result,

        "privacy_analysis": privacy_result,

        "security_analysis": security_result,

        "fairness_analysis": fairness_result,

        "operational_analysis": operational_result,

        "final_stress_result": final_result
    }

# --------------------------------------------------
# Privacy Analysis Endpoint
# --------------------------------------------------
@app.post("/api/generate-report")
def generate_report(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    solution = request.solution

    # ---------------------------------------------
    # 1. Solution Understanding
    # ---------------------------------------------

    understanding = solution_agent.analyze(
        solution
    )

    # ---------------------------------------------
    # 2. Technical Analysis
    # ---------------------------------------------

    technical_result = technical_agent.analyze(
        solution,
        understanding
    )

    # ---------------------------------------------
    # 3. Cost Analysis
    # ---------------------------------------------

    cost_result = cost_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ---------------------------------------------
    # 4. Privacy Analysis
    # ---------------------------------------------

    privacy_result = privacy_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ---------------------------------------------
    # 5. Security Analysis
    # ---------------------------------------------

    security_result = security_agent.analyze(
        solution,
        understanding,
        technical_result,
        privacy_result
    )

    # ---------------------------------------------
    # 6. Fairness Analysis
    # ---------------------------------------------

    fairness_result = fairness_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ---------------------------------------------
    # 7. Operational Analysis
    # ---------------------------------------------

    operational_result = operational_agent.analyze(
        solution,
        understanding,
        technical_result
    )

    # ---------------------------------------------
    # 8. Stress Judge
    # ---------------------------------------------

    final_result = stress_judge.evaluate(
        solution,
        understanding,
        technical_result,
        cost_result,
        privacy_result,
        security_result,
        fairness_result,
        operational_result
    )

    # ---------------------------------------------
    # 9. Final Report
    # ---------------------------------------------

    report = report_generator.generate(
        solution,
        understanding,
        final_result
    )

    return {
        "success": True,

        "solution": solution,

        "final_stress_result": final_result,

        "final_report": report
    }





@app.post("/api/analyze")
def analyze_solution(request: SolutionRequest):

    if not request.solution.strip():

        return {
            "success": False,
            "error": "Solution description cannot be empty."
        }

    try:

        result = workflow.run(
            request.solution
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }