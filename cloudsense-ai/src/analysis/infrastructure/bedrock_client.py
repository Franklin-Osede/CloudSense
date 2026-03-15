import boto3
import json
import logging
from typing import List, Dict
from src.analysis.domain.models import Anomaly

class ClaudeBedrockClient:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'

    def analyze_anomalies(self, anomalies: List[Anomaly]) -> Dict:
        """
        Calls AWS Bedrock Claude model to analyze cost anomalies.
        """
        if not anomalies:
            return {"summary": "No anomalies to analyze."}

        anomaly_details = "\\n".join(
            [f"- {a.service_name}: Expected ${a.expected_amount:.2f}, Actual ${a.actual_amount:.2f}. Reason: {a.reason}" for a in anomalies]
        )
        
        prompt = f"""You are a Senior Cloud FinOps expert. Analyze the following AWS cost anomalies and provide a brief, actionable summary explaining potential causes and recommendations:

Anomalies:
{anomaly_details}

Return ONLY a concise paragraph. Do not include introductory text."""

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }),
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            summary_text = response_body.get('content', [{}])[0].get('text', 'No analysis generated.')
            
            return {
                "summary": f"Claude Analysis: {summary_text}"
            }
            
        except Exception as e:
            logging.error(f"Error invoking Bedrock: {e}")
            return {
                "summary": "AI analysis currently unavailable due to an error connecting to AWS Bedrock."
            }
