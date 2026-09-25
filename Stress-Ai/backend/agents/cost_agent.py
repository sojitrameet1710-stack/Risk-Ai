import json
import re
from groq import Groq


class CostResourceAgent:

    def __init__(self, client: Groq):
        self.client = client

    def analyze(self, solution, understanding, technical_analysis):

        prompt = f"""
You are the Cost and Resource Stress Agent inside an AI Solution Stress Tester.

Your job is to determine whether a proposed solution is financially and
resource-wise practical.

Do NOT invent exact market prices.

If exact costs are unknown, use relative estimates such as:
Low, Medium, High, or Very High.

PROPOSED SOLUTION:
{solution}

SOLUTION UNDERSTANDING:
{json.dumps(understanding, indent=2)}

TECHNICAL ANALYSIS:
{json.dumps(technical_analysis, indent=2)}

Evaluate:

1. Development cost
2. Infrastructure requirements
3. AI/LLM usage cost
4. Database/storage requirements
5. Human resources required
6. Maintenance requirements
7. Scaling cost
8. Resource bottlenecks
9. Hidden costs
10. Cost reduction recommendations

Return ONLY valid JSON:

{{
    "overall_cost_level": "Low/Medium/High/Very High",

    "development_cost": {{
        "level": "",
        "reason": ""
    }},

    "infrastructure_cost": {{
        "level": "",
        "reason": ""
    }},

    "ai_cost": {{
        "level": "",
        "reason": ""
    }},

    "storage_cost": {{
        "level": "",
        "reason": ""
    }},

    "human_resource_requirements": [],

    "maintenance_requirements": [],

    "scaling_cost_risk": "Low/Medium/High",

    "resource_bottlenecks": [],

    "hidden_costs": [],

    "cost_risks": [],

    "cost_reduction_recommendations": []
}}

Rules:
- Do not provide fake exact prices.
- Use relative cost levels.
- Consider both small-scale and large-scale deployment.
- Identify hidden resource requirements.
- Be critical.
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical AI cost and resource analyst."
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