from datetime import date
from typing import List, Dict

class FakeAwsCostClient:
    def get_cost_and_usage(self, start_date: date, end_date: date) -> List[Dict]:
        """
        Simulates returning cost data from AWS Cost Explorer.
        Injected with realistic anomalies for the demo.
        """
        # Normal usage is around $150/day. On anomalous days, it spikes to $500+.
        is_anomaly_day = start_date.weekday() >= 5 # Simulating a weekend spike
        
        ec2_cost = 400.0 if is_anomaly_day else 100.0
        
        return [
            {
                "account_id": "123456789012",
                "date": start_date,
                "services": [
                    {"name": "AmazonEC2", "amount": ec2_cost},
                    {"name": "AmazonRDS", "amount": 35.0},
                    {"name": "AmazonS3", "amount": 15.0}
                ]
            }
        ]
