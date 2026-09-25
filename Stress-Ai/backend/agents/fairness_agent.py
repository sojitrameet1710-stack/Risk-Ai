import json
import re
from groq import Groq


class FairnessRiskAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(
        self,
        solution,
        understanding,
        technical_analysis
    ):

        prompt = f"""
You are the Bias and Fairness Risk Agent inside an AI Solution Stress Tester.

Your job is to critically evaluate whether a proposed AI solution
could produce biased, discriminatory, or unfair outcomes.

Do not assume bias automatically exists.

Identify potential bias based on:
- Data
- Features
- Historical decisions
- User groups
- Model outputs
- Deployment context

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

TECHNICAL ANALYSIS:
{json.dumps(technical_analysis, indent=2)}

Evaluate:

1. Potential sources of bias
2. Historical bias
3. Dataset representation risks
4. Feature/proxy risks
5. Group fairness risks
6. Outcome disparity risks
7. Measurement challenges
8. Feedback-loop risks
9. Human decision-making risks
10. Fairness monitoring requirements
11. Bias mitigation recommendations

Return ONLY valid JSON:

{{
    "fairness_risk_level": "Low/Medium/High/Critical",

    "potential_bias_sources": [],

    "historical_bias_risks": [],

    "representation_risks": [],

    "feature_proxy_risks": [],

    "group_fairness_risks": [],

    "outcome_disparity_risks": [],

    "measurement_challenges": [],

    "feedback_loop_risks": [],

    "human_decision_risks": [],

    "fairness_monitoring_requirements": [],

    "bias_mitigation_recommendations": []
}}

Rules:
- Do not claim that a solution is biased without evidence.
- Clearly distinguish potential risks from confirmed bias.
- Consider different user groups where relevant.
- Do not provide the final overall stress-test score.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical AI fairness and bias analyst."
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