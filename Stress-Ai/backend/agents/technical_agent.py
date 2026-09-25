import json
import re
from groq import Groq


class TechnicalFeasibilityAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(self, solution, understanding):

        prompt = f"""
You are the Technical Feasibility Agent inside an AI Solution Stress Tester.

Your job is NOT to blindly approve a solution.

You must critically evaluate whether the proposed solution is technically feasible.

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

Analyze:

1. Technical feasibility
2. Required technology
3. Required data
4. System complexity
5. Integration requirements
6. Scalability concerns
7. Technical risks
8. Possible failure points
9. Missing technical requirements
10. Recommendations

Return ONLY valid JSON:

{{
    "feasibility": "High/Medium/Low",
    "technology_requirements": [],
    "data_requirements": [],
    "system_components": [],
    "integration_requirements": [],
    "complexity_level": "Low/Medium/High",
    "scalability_risks": [],
    "technical_risks": [],
    "failure_points": [],
    "missing_requirements": [],
    "recommendations": []
}}

Rules:
- Be critical.
- Do not assume unlimited resources.
- Identify unrealistic assumptions.
- If information is missing, mention it.
- Do not give the final overall stress-test score.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical technical feasibility analyst."
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