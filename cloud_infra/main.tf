terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDB Table for storing embeddings and traces
resource "aws_dynamodb_table" "composemind_table" {
  name           = "composemind-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "composemind_api" {
  name          = "composemind-api"
  protocol_type = "HTTP"
}

# Lambda function for composition engine
resource "aws_lambda_function" "composition_engine" {
  filename         = "../composition_engine/lambda.zip"
  function_name    = "composition-engine"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 256
}

# IAM role for Lambda
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

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
} 