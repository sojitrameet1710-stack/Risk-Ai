from backend.agents.solution_analyzer import SolutionUnderstandingAgent
from backend.agents.technical_agent import TechnicalFeasibilityAgent
from backend.agents.cost_agent import CostResourceAgent
from backend.agents.privacy_agent import PrivacyRiskAgent
from backend.agents.security_agent import SecurityRiskAgent
from backend.agents.fairness_agent import FairnessRiskAgent
from backend.agents.operational_agent import OperationalReliabilityAgent
from backend.agents.stress_judge import StressJudgeAgent
from backend.agents.report_generator import ReportGeneratorAgent


class StressTestWorkflow:

    def __init__(self, client):

        self.solution_agent = SolutionUnderstandingAgent(client)
        self.technical_agent = TechnicalFeasibilityAgent(client)
        self.cost_agent = CostResourceAgent(client)
        self.privacy_agent = PrivacyRiskAgent(client)
        self.security_agent = SecurityRiskAgent(client)
        self.fairness_agent = FairnessRiskAgent(client)
        self.operational_agent = OperationalReliabilityAgent(client)

        self.stress_judge = StressJudgeAgent(client)
        self.report_generator = ReportGeneratorAgent(client)

    def run(self, solution):

        # --------------------------------
        # 1. Understanding
        # --------------------------------

        understanding = self.solution_agent.analyze(
            solution
        )

        # --------------------------------
        # 2. Technical
        # --------------------------------

        technical = self.technical_agent.analyze(
            solution,
            understanding
        )

        # --------------------------------
        # 3. Cost
        # --------------------------------

        cost = self.cost_agent.analyze(
            solution,
            understanding,
            technical
        )

        # --------------------------------
        # 4. Privacy
        # --------------------------------

        privacy = self.privacy_agent.analyze(
            solution,
            understanding,
            technical
        )

        # --------------------------------
        # 5. Security
        # --------------------------------

        security = self.security_agent.analyze(
            solution,
            understanding,
            technical,
            privacy
        )

        # --------------------------------
        # 6. Fairness
        # --------------------------------

        fairness = self.fairness_agent.analyze(
            solution,
            understanding,
            technical
        )

        # --------------------------------
        # 7. Operational
        # --------------------------------

        operational = self.operational_agent.analyze(
            solution,
            understanding,
            technical
        )

        # --------------------------------
        # 8. FINAL JUDGE
        # --------------------------------

        final_result = self.stress_judge.evaluate(
            solution,
            technical,
            cost,
            privacy,
            security,
            fairness,
            operational
        )

        # --------------------------------
        # 9. REPORT
        # --------------------------------

        report = self.report_generator.generate(
            solution,
            final_result
        )

        return {
            "solution": solution,
            "understanding": understanding,
            "technical": technical,
            "cost": cost,
            "privacy": privacy,
            "security": security,
            "fairness": fairness,
            "operational": operational,
            "final_result": final_result,
            "report": report
        }