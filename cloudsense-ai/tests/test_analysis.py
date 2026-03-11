import pytest
from datetime import date
from src.analysis.domain.models import Anomaly

def test_anomaly_detection_logic():
    # Test valid creation of an anomaly
    anomaly = Anomaly(
        account_id="123456789012",
        date=date(2026, 3, 11),
        service_name="AmazonEC2",
        expected_amount=100.0,
        actual_amount=300.0,
        reason="Unexpected spike in EC2 usage"
    )
    
    assert anomaly.actual_amount > anomaly.expected_amount
    assert anomaly.service_name == "AmazonEC2"
