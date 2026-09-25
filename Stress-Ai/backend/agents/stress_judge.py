import json
import re
from groq import Groq


class StressJudgeAgent:

    def __init__(self, client: Groq):
        self.client = client

    def evaluate(
        self,
        solution,
        technical,
        cost,
        privacy,
        security,
        fairness,
        operational
    ):

        # Only send compact summaries to the final judge
        analysis_summary = {
            "technical": technical,
            "cost": cost,
            "privacy": privacy,
            "security": security,
            "fairness": fairness,
            "operational": operational
        }

        prompt = f"""
You are the final judge of an AI Solution Stress Tester.

Evaluate the proposed solution using the risk summaries below.

SOLUTION:
{solution[:2000]}

RISK SUMMARIES:
{json.dumps(analysis_summary, indent=2)[:12000]}

Return ONLY valid JSON:

{{
    "stress_score": 0,
    "risk_level": "Very Low/Low/Medium/High/Critical",
    "decision": "Proceed/Proceed with Caution/Needs Major Changes/Do Not Proceed",

    "dimension_scores": {{
        "technical": 0,
        "cost": 0,
        "privacy": 0,
        "security": 0,
        "fairness": 0,
        "operational": 0
    }},

    "top_risks": [],
    "critical_blockers": [],
    "strengths": [],
    "recommended_actions": [],
    "overall_reasoning": ""
}}

Scoring:

0-20   Very Low
21-40  Low
41-60  Medium
61-80  High
81-100 Critical

Important:
- stress_score must be 0-100.
- Each dimension score must be 0-100.
- Do not invent facts.
- Prioritize serious security, privacy and operational risks.
- Return JSON only.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI risk scoring judge."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=1500
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL
            )

            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

            return {
                "raw_analysis": content
            }