from typing import List
from datetime import date
from src.analysis.domain.models import Anomaly, Recommendation, AnalysisResult
from src.billing.domain.models import CostData
from src.analysis.infrastructure.bedrock_client import ClaudeBedrockClient

class DetectAnomalyUseCase:
    def __init__(self, ai_client: ClaudeBedrockClient):
        self.ai_client = ai_client
        self.anomaly_threshold_percent = 50.0 # Flag if 50% above expected

    def execute(self, cost_data: CostData, expected_daily_cost: float) -> AnalysisResult:
        anomalies = []
        
        for account in cost_data.accounts:
            for service in account.services:
                # Naive expectation: expected cost divided equally by 3 services
                expected_service = expected_daily_cost / 3
                
                if expected_service > 0:
                    percent_increase = ((service.amount - expected_service) / expected_service) * 100
                    if percent_increase >= self.anomaly_threshold_percent:
                        anomalies.append(
                            Anomaly(
                                account_id=account.account_id,
                                date=account.date,
                                service_name=service.service_name,
                                expected_amount=expected_service,
                                actual_amount=service.amount,
                                reason=f"Cost increased by {percent_increase:.1f}% above expected baseline"
                            )
                        )
                        
        # If anomalies found, ask Bedrock for recommendations
        recommendations = []
        summary = "No anomalies detected."
        
        if anomalies:
            analysis_response = self.ai_client.analyze_anomalies(anomalies)
            summary = analysis_response["summary"]
            
            # Create a parsed recommendation
            for anom in anomalies:
                recommendations.append(
                    Recommendation(
                        account_id=anom.account_id,
                        service_name=anom.service_name,
                        action="Investigate and terminate unused resources.",
                        estimated_savings=anom.actual_amount - anom.expected_amount
                    )
                )

        return AnalysisResult(
            anomalies=anomalies,
            recommendations=recommendations,
            summary_text=summary
        )
