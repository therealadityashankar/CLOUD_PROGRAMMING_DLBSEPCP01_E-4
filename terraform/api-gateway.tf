resource "aws_apigatewayv2_api" "image_api" {
  provider      = aws.eu_central_1
  name          = "image-service-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "image_api_stage" {
  provider    = aws.eu_central_1
  api_id      = aws_apigatewayv2_api.image_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  provider           = aws.eu_central_1
  api_id             = aws_apigatewayv2_api.image_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.image_service.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "catch_all_route" {
  provider  = aws.eu_central_1
  api_id    = aws_apigatewayv2_api.image_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gateway_permission" {
  provider      = aws.eu_central_1
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.image_api.execution_arn}/*/*"
}

# Output the API Gateway URLs
output "api_gateway_url" {
  value = aws_apigatewayv2_stage.image_api_stage.invoke_url
  description = "Base API Gateway URL"
}

output "image_url_example" {
  value = "${aws_apigatewayv2_stage.image_api_stage.invoke_url}cat0.jpg"
  description = "Example URL for accessing an image"
}

output "view_url" {
  value = "${aws_apigatewayv2_stage.image_api_stage.invoke_url}view?index=0"
  description = "URL for the image viewer interface"
}

output "rankings_url" {
  value = "${aws_apigatewayv2_stage.image_api_stage.invoke_url}rankings"
  description = "URL for the image rankings page"
} 