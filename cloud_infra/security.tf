# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "composemind_lambda_role"

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

# IAM policy for DynamoDB access
resource "aws_iam_policy" "dynamodb_access" {
  name        = "composemind_dynamodb_access"
  description = "Allow access to DynamoDB tables"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.composemind_table.arn
      }
    ]
  })
}

# IAM policy for CloudWatch Logs
resource "aws_iam_policy" "cloudwatch_logs" {
  name        = "composemind_cloudwatch_logs"
  description = "Allow writing to CloudWatch Logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach policies to Lambda role
resource "aws_iam_role_policy_attachment" "dynamodb_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}

resource "aws_iam_role_policy_attachment" "cloudwatch_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch_logs.arn
}

# API Gateway authorizer
resource "aws_apigatewayv2_authorizer" "jwt" {
  api_id           = aws_apigatewayv2_api.composemind_api.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name            = "jwt-authorizer"

  jwt_configuration {
    audience = ["composemind-api"]
    issuer   = "https://cognito-idp.${var.aws_region}.amazonaws.com/${aws_cognito_user_pool.pool.id}"
  }
} 