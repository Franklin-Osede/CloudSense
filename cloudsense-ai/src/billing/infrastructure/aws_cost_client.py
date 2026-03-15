import boto3
from datetime import date, timedelta
from typing import List, Dict
import logging

class AwsCostClient:
    def __init__(self):
        self.ce_client = boto3.client('ce', region_name='us-east-1')

    def get_cost_and_usage(self, start_date: date, end_date: date) -> List[Dict]:
        """
        Fetches real cost data from AWS Cost Explorer.
        """
        # Cost Explorer requires the end date to be exclusive so we add 1 day
        ce_end_date = end_date + timedelta(days=1)
        
        try:
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': ce_end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'}
                ]
            )
            
            # For demonstration purposes, we assume a single account structure.
            # In a multi-account environment, we would also GroupBy LINKED_ACCOUNT.
            
            accounts_data = []
            
            for result_by_time in response['ResultsByTime']:
                current_date = result_by_time['TimePeriod']['Start']
                services = []
                
                for group in result_by_time['Groups']:
                    service_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    
                    if amount > 0:
                        services.append({
                            "name": service_name,
                            "amount": amount
                        })
                
                # Mocking account ID for the demo since we didn't group by it
                accounts_data.append({
                    "account_id": "123456789012",
                    "date": date.fromisoformat(current_date),
                    "services": services
                })
                
            return accounts_data
            
        except Exception as e:
            logging.error(f"Error fetching Cost Explorer data: {e}")
            return []
