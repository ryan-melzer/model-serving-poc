provider "aws" {
  region = var.region

  assume_role {
    role_arn = var.workspace_role_arn
  }

  default_tags {
    tags = local.default_tags
  }

}