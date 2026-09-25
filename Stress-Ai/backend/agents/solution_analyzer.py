import json
import re
from groq import Groq


class SolutionUnderstandingAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(self, solution: str):

        prompt = f"""
You are the Solution Understanding Agent of an AI Solution Stress Tester.

Your job is to understand a proposed real-world solution before it is stress-tested.

Analyze the following proposed solution:

--- SOLUTION ---
{solution}
--- END SOLUTION ---

Return ONLY valid JSON with these fields:

{{
    "problem_statement": "",
    "target_users": [],
    "proposed_solution": "",
    "key_features": [],
    "required_inputs": [],
    "expected_outputs": [],
    "assumptions": [],
    "dependencies": [],
    "success_criteria": [],
    "initial_concerns": [],
    "ambiguities": []
}}

Rules:
- Do not invent facts that are not reasonably implied.
- If information is missing, mention it in "ambiguities".
- Keep the analysis practical.
- Keep each list concise.
- Avoid unnecessary explanations.
- Return only the requested JSON.
- Identify assumptions clearly.
- Do not provide the final stress-test result yet.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise AI solution analysis agent."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1800,
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            # Try extracting JSON if the model added extra text
            match = re.search(r"\{.*\}", content, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

            return {
                "raw_analysis": content
            }