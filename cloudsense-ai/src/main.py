from datetime import date, timedelta
import logging
import json

from src.billing.infrastructure.aws_cost_client import AwsCostClient
from src.billing.application.fetch_costs import FetchCostsUseCase
from src.analysis.infrastructure.bedrock_client import ClaudeBedrockClient
from src.analysis.application.detect_anomaly import DetectAnomalyUseCase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting CloudSense AI - Cost Collection Cycle")
    
    # 1. Setup Clients & Use Cases
    cost_client = AwsCostClient()
    fetch_costs_uc = FetchCostsUseCase(cost_client)
    
    bedrock_client = ClaudeBedrockClient()
    detect_anomaly_uc = DetectAnomalyUseCase(bedrock_client)
    
    # 2. Simulate date (Let's pretend today is a Sunday to trigger the anomaly)
    # 2026-03-15 is a Sunday
    simulated_date = date(2026, 3, 15)
    
    # 3. Fetch Data
    logging.info(f"Fetching AWS Cost Explorer data for {simulated_date}...")
    cost_data = fetch_costs_uc.execute(start_date=simulated_date, end_date=simulated_date)
    
    # 4. Analyze Data
    logging.info("Analyzing cost data for anomalies using AWS Bedrock...")
    expected_daily = 150.0 # Baseline expectation
    analysis_result = detect_anomaly_uc.execute(cost_data, expected_daily)
    
    # 5. Output Results (In a real app, this goes to SNS, Slack, or Grafana via prometheus metrics/Loki logs)
    logging.info("--- ANALYSIS RESULTS ---")
    if analysis_result.anomalies:
        logging.warning(f"Found {len(analysis_result.anomalies)} anomalies!")
        for anomaly in analysis_result.anomalies:
            logging.warning(f"  - {anomaly.service_name}: Expected ${anomaly.expected_amount:.2f}, Actual ${anomaly.actual_amount:.2f}")
    
    logging.info(f"AI Summary: {analysis_result.summary_text}")
    
    for rec in analysis_result.recommendations:
        logging.info(f"Recommendation for {rec.service_name}: {rec.action} (Est. Savings: ${rec.estimated_savings:.2f})")
        
    # Output JSON for Loki parsing if needed
    print(analysis_result.model_dump_json())

if __name__ == "__main__":
    main()
