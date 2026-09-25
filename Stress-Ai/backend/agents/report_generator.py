import json
import re
from groq import Groq


class ReportGeneratorAgent:

    def __init__(self, client: Groq):
        self.client = client

    def generate(
        self,
        solution,
        final_result
    ):

        prompt = f"""
Create a concise professional AI Solution Stress Test report.

SOLUTION:
{solution[:2000]}

FINAL RESULT:
{json.dumps(final_result, indent=2)[:7000]}

Return ONLY valid JSON:

{{
    "title": "AI Solution Stress Test Report",
    "executive_summary": "",
    "overall_assessment": "",
    "stress_score_explanation": "",

    "risk_breakdown": [],

    "critical_issues": [],
    "strengths": [],
    "recommended_actions": [],

    "final_verdict": "",
    "verdict_type": ""
}}

Rules:
- Do not change the score.
- Do not invent information.
- Keep responses concise.
- Return JSON only.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You create concise AI risk reports."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1200
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
                "raw_report": content
            }