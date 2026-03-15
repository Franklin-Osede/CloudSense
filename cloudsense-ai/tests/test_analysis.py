import pytest
from datetime import date
from unittest.mock import Mock

from src.analysis.application.detect_anomaly import DetectAnomalyUseCase
from src.billing.domain.models import CostData, AccountSpend, ServiceCost
from src.analysis.infrastructure.bedrock_client import ClaudeBedrockClient

def test_detect_anomaly_triggers_alert_on_spike():
    # Arrange
    mock_bedrock = Mock(spec=ClaudeBedrockClient)
    mock_bedrock.analyze_anomalies.return_value = {"summary": "Mock summary"}
    
    use_case = DetectAnomalyUseCase(mock_bedrock)
    
    # Simulate a day with expected cost $150 (each service $50 expected)
    # But EC2 costs $400, which is an 800% increase
    cost_data = CostData(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 1),
        accounts=[
            AccountSpend(
                account_id="123",
                date=date(2026, 3, 1),
                total_amount=400.0,
                services=[
                    ServiceCost(service_name="AmazonEC2", amount=400.0)
                ]
            )
        ]
    )
    
    # Act
    result = use_case.execute(cost_data, expected_daily_cost=150.0)
    
    # Assert
    assert len(result.anomalies) == 1
    assert result.anomalies[0].service_name == "AmazonEC2"
    assert result.anomalies[0].actual_amount == 400.0
    assert result.summary_text == "Mock summary"
    mock_bedrock.analyze_anomalies.assert_called_once()

def test_detect_anomaly_no_spike():
    # Arrange
    mock_bedrock = Mock(spec=ClaudeBedrockClient)
    
    use_case = DetectAnomalyUseCase(mock_bedrock)
    
    cost_data = CostData(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 1),
        accounts=[
            AccountSpend(
                account_id="123",
                date=date(2026, 3, 1),
                total_amount=45.0,
                services=[
                    ServiceCost(service_name="AmazonEC2", amount=45.0)
                ]
            )
        ]
    )
    
    # Act
    # expected_daily_cost=150 / 3 = 50 per service expected
    # 45 is less than 50, so no anomaly
    result = use_case.execute(cost_data, expected_daily_cost=150.0)
    
    # Assert
    assert len(result.anomalies) == 0
    assert result.summary_text == "No anomalies detected."
    mock_bedrock.analyze_anomalies.assert_not_called()
