import json
import re
from groq import Groq


class SecurityRiskAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(
        self,
        solution,
        understanding,
        technical_analysis,
        privacy_analysis
    ):

        prompt = f"""
You are the Security Risk Agent inside an AI Solution Stress Tester.

Your job is to critically evaluate cybersecurity risks in a proposed
AI-powered solution.

Do NOT assume that every possible vulnerability exists.
Identify risks based on the actual solution and its architecture.

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

TECHNICAL ANALYSIS:
{json.dumps(technical_analysis, indent=2)}

PRIVACY ANALYSIS:
{json.dumps(privacy_analysis, indent=2)}

Evaluate:

1. Authentication risks
2. Authorization/access-control risks
3. API security risks
4. Data security risks
5. AI/LLM-specific security risks
6. Input validation risks
7. Prompt injection risks if an LLM is involved
8. Secrets/API-key exposure risks
9. Infrastructure security risks
10. Logging and monitoring weaknesses
11. Abuse/misuse risks
12. Single points of failure
13. Security recommendations

Return ONLY valid JSON:

{{
    "security_risk_level": "Low/Medium/High/Critical",

    "authentication_risks": [],

    "authorization_risks": [],

    "api_security_risks": [],

    "data_security_risks": [],

    "ai_security_risks": [],

    "input_validation_risks": [],

    "prompt_injection_risks": [],

    "secret_exposure_risks": [],

    "infrastructure_risks": [],

    "logging_monitoring_risks": [],

    "abuse_risks": [],

    "single_points_of_failure": [],

    "security_weaknesses": [],

    "security_recommendations": []
}}

Rules:
- Be practical and critical.
- Do not invent vulnerabilities without a reasonable basis.
- Distinguish between confirmed and potential risks.
- Never reveal or request actual API keys, passwords, or secrets.
- Do not provide the final overall stress-test score.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity risk analysis agent."
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