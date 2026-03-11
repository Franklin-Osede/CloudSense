from typing import List, Dict
from src.analysis.domain.models import Anomaly

class ClaudeBedrockClient:
    def analyze_anomalies(self, anomalies: List[Anomaly]) -> Dict:
        """
        Simulates a call to AWS Bedrock Claude model.
        In a real app, uses boto3 bedrock-runtime invoke_model.
        """
        prompt = "Analyze the following cost anomalies: " + ", ".join([a.service_name for a in anomalies])
        
        # Simulating the LLM response
        return {
            "summary": f"Claude Analysis: Detected abnormal spikes in '{', '.join([a.service_name for a in anomalies])}'. " \
                       "Recommendation: Verify if a new deployment was left running over the weekend without auto-scaling down."
        }
