import json
import re
from groq import Groq


class OperationalReliabilityAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(
        self,
        solution,
        understanding,
        technical_analysis
    ):

        prompt = f"""
You are the Operational and Reliability Stress Agent
inside an AI Solution Stress Tester.

Your job is to evaluate whether a proposed solution can
reliably operate in the real world after deployment.

Focus on operational and reliability risks.

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

TECHNICAL ANALYSIS:
{json.dumps(technical_analysis, indent=2)}

Evaluate:

1. System reliability
2. Availability and downtime risks
3. Performance risks
4. Scalability risks
5. External dependency risks
6. Failure recovery
7. Monitoring requirements
8. Maintenance requirements
9. Human dependency
10. Disaster recovery
11. Single points of failure
12. Long-term operational risks
13. Reliability recommendations

Return ONLY valid JSON:

{{
    "operational_risk_level": "Low/Medium/High/Critical",

    "reliability_risks": [],

    "availability_risks": [],

    "performance_risks": [],

    "scalability_risks": [],

    "external_dependency_risks": [],

    "failure_recovery_risks": [],

    "monitoring_requirements": [],

    "maintenance_requirements": [],

    "human_dependency_risks": [],

    "disaster_recovery_risks": [],

    "single_points_of_failure": [],

    "long_term_risks": [],

    "reliability_recommendations": []
}}

Rules:
- Be practical and critical.
- Do not invent dependencies that are not relevant.
- Distinguish between potential and confirmed risks.
- Consider both initial deployment and future scaling.
- Do not provide the final overall stress-test score.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a critical operational reliability "
                        "and system resilience analyst."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            match = re.search(r"\{.*\}", content, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

            return {
                "raw_analysis": content
            }