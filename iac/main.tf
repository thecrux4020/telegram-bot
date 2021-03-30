terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  backend "s3" {
    region = "us-east-1"
    bucket = "telegram-bot-terraform-iac"
    key = "state/terraform.tfstate"

    # Change profile based on your ~/.aws/credentials configuration
    profile = "mantux"
  }

}