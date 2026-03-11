# IAM Role for AWS Lambda (Cost Collector & Anomaly Detector)
resource "aws_iam_role" "lambda_exec_role" {
  name = "cloudsense_lambda_exec_role_${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Allow Bedrock access for Anomaly Detection
resource "aws_iam_role_policy" "bedrock_access" {
  name = "cloudsense_bedrock_access"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "bedrock:InvokeModel"
        ]
        Effect   = "Allow"
        Resource = "*" # Restrict to specific Claude model ARN in production
      }
    ]
  })
}
