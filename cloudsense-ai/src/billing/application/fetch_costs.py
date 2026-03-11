from typing import List
from datetime import date
from src.billing.domain.models import CostData, AccountSpend, ServiceCost
from src.billing.infrastructure.aws_cost_client import FakeAwsCostClient

class FetchCostsUseCase:
    def __init__(self, cost_client: FakeAwsCostClient):
        self.cost_client = cost_client

    def execute(self, start_date: date, end_date: date) -> CostData:
        # In a real app, this would handle pagination, error retries, caching etc.
        raw_data = self.cost_client.get_cost_and_usage(start_date, end_date)
        
        accounts = []
        for raw_acc in raw_data:
            services = [
                ServiceCost(service_name=s["name"], amount=s["amount"])
                for s in raw_acc["services"]
            ]
            
            acc_spend = AccountSpend(
                account_id=raw_acc["account_id"],
                date=raw_acc["date"],
                total_amount=sum(s.amount for s in services),
                services=services
            )
            accounts.append(acc_spend)

        return CostData(
            start_date=start_date,
            end_date=end_date,
            accounts=accounts
        )
