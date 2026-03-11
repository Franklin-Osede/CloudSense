import pytest
from datetime import date
from src.billing.domain.models import AccountSpend, ServiceCost, CostData

def test_account_spend_creation():
    spend = AccountSpend(
        account_id="123456789012",
        date=date(2026, 3, 11),
        total_amount=150.50,
        services=[
            ServiceCost(service_name="AmazonEC2", amount=100.00),
            ServiceCost(service_name="AmazonRDS", amount=50.50)
        ]
    )
    assert spend.account_id == "123456789012"
    assert len(spend.services) == 2
    assert spend.total_amount == 150.50

def test_cost_data_validation():
    # Test valid creation
    data = CostData(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 11),
        accounts=[]
    )
    assert data.start_date < data.end_date
