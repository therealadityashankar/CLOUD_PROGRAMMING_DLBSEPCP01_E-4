resource "aws_apigatewayv2_api" "image_api" {
  name          = "image-service-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "image_api_stage" {
  api_id      = aws_apigatewayv2_api.image_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.image_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.image_service.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "image_route" {
  api_id    = aws_apigatewayv2_api.image_api.id
  route_key = "GET /{image}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.image_api.execution_arn}/*/*/{image}"
}

# Output the API Gateway URL
# this gives the output upon deployment
output "api_gateway_url" {
  value = aws_apigatewayv2_stage.image_api_stage.invoke_url
} 