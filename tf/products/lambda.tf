provider "aws" {
  region = "ap-northeast-1"
}

module "fof_state_launch" {
  env = var.env
  source = "./modules/lambda/"
  function_name = "fof_state_launch"
  memory = 128
  description = ""
  environment = merge(var.lambda_environment_default, {
    "hoge" = "fuga"
  })
  layer_arn = module.fof_sdk.arn
  external_module_layer_arn = data.aws_lambda_layer_version.external_module_layer.arn
  role = var.lambda_role
}

module "fof_sdk" {
  env = var.env
  source = "./modules/lambda_layer"
}

// TODO var.env 入れたい
data "aws_lambda_layer_version" "external_module_layer" {
  layer_name = "alexa-packages"
}