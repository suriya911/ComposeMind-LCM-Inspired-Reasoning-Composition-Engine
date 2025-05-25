# API Gateway
resource "aws_apigatewayv2_api" "composemind_api" {
  name          = "composemind-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
  }
}

# API Gateway stage
resource "aws_apigatewayv2_stage" "prod" {
  api_id = aws_apigatewayv2_api.composemind_api.id
  name   = "prod"
  auto_deploy = true
}

# API Gateway integration for composition engine
resource "aws_apigatewayv2_integration" "composition_engine" {
  api_id           = aws_apigatewayv2_api.composemind_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.composition_engine.invoke_arn
}

# API Gateway integration for trace service
resource "aws_apigatewayv2_integration" "trace_service" {
  api_id           = aws_apigatewayv2_api.composemind_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.trace_service.invoke_arn
}

# API Gateway routes
resource "aws_apigatewayv2_route" "compose" {
  api_id    = aws_apigatewayv2_api.composemind_api.id
  route_key = "POST /compose"
  target    = "integrations/${aws_apigatewayv2_integration.composition_engine.id}"
}

resource "aws_apigatewayv2_route" "trace" {
  api_id    = aws_apigatewayv2_api.composemind_api.id
  route_key = "GET /trace/{traceId}"
  target    = "integrations/${aws_apigatewayv2_integration.trace_service.id}"
}

# API Gateway permissions
resource "aws_lambda_permission" "composition_engine" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.composition_engine.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.composemind_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "trace_service" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trace_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.composemind_api.execution_arn}/*/*"
} 