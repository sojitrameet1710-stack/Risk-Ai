import json
import re
from groq import Groq


class PrivacyRiskAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(self, solution, understanding, technical_analysis):

        prompt = f"""
You are the Privacy and Data Risk Agent inside an AI Solution Stress Tester.

Your job is to critically evaluate privacy and data-related risks
in a proposed AI solution.

Do NOT automatically assume that every solution has sensitive data.

Identify the actual data requirements and potential privacy risks.

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

TECHNICAL ANALYSIS:
{json.dumps(technical_analysis, indent=2)}

Evaluate:

1. Data collected
2. Personal data
3. Potentially sensitive data
4. Data ownership
5. User consent requirements
6. Data storage risks
7. Data access risks
8. Data sharing risks
9. Third-party/API data exposure
10. Data retention concerns
11. Data leakage risks
12. Privacy weaknesses
13. Privacy recommendations

Return ONLY valid JSON:

{{
    "privacy_risk_level": "Low/Medium/High/Critical",

    "data_collected": [],

    "personal_data": [],

    "sensitive_data": [],

    "data_ownership_concerns": [],

    "consent_requirements": [],

    "data_storage_risks": [],

    "data_access_risks": [],

    "data_sharing_risks": [],

    "third_party_data_risks": [],

    "data_retention_concerns": [],

    "data_leakage_risks": [],

    "privacy_weaknesses": [],

    "privacy_recommendations": []
}}

Rules:
- Do not invent data that the solution does not require.
- Clearly distinguish confirmed data requirements from possible data.
- Be critical but practical.
- Do not provide legal advice.
- Do not provide the final overall stress-test score.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical AI privacy and data risk analyst."
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