
resource "aws_cloudwatch_event_target" "lambda_poll" {
  target_id = "lambda_poll"
  rule      = aws_cloudwatch_event_rule.crontab.name
  arn       = aws_lambda_function.telegram_polls_lambda.arn
}

resource "aws_cloudwatch_event_rule" "crontab" {
    name = "crontab"
    event_bus_name      = "default"
    is_enabled          = true
    schedule_expression = "cron(0 9 * * ? *)"
}

resource "aws_lambda_function" "telegram_polls_lambda" {
    function_name = "telegram-poll"
    description = "Polls job to send telegram quizz"
    handler = "main.lambda_handler"
    memory_size = 128
    package_type = "Zip"
    reserved_concurrent_executions = -1
    role = aws_iam_role.iam_for_lambda.arn
    runtime = "python3.6"
    source_code_hash = filebase64sha256("${path.module}/../scripts/build/deploy.zip")
    filename = "${path.module}/../scripts/build/deploy.zip"
    timeout = 60
    environment {
        variables = {
            "JOB_NAME" = "POLL"
            "TELEGRAM_TOKEN" = var.telegram_token
        }
    }

}

resource "aws_iam_role" "iam_for_lambda" {
    name = "telegram-poll-role-1rw8qxlz"
    assume_role_policy = jsonencode(
        {
            Statement = [
                {
                    Action = "sts:AssumeRole"
                    Effect = "Allow"
                    Principal = {
                        Service = "lambda.amazonaws.com"
                    }
                },
            ]
            Version = "2012-10-17"
        }
    )
    path = "/service-role/"
    inline_policy {
        name = "dynamo-read-write-limited"
        policy = jsonencode(
            {
                Statement = [
                    {
                        Action = [
                            "dynamodb:Scan",
                            "dynamodb:UpdateItem",
                        ]
                        Effect = "Allow"
                        Resource = "arn:aws:dynamodb:*:543960471003:table/quizzes_questions"
                    },
                ]
                Version = "2012-10-17"
            }
        )
    }


}

resource "aws_dynamodb_table" "bot_quizzes_table" {
    name = "quizzes_questions"
    billing_mode = "PROVISIONED"
    hash_key = "question_id"
    read_capacity = 1
    stream_enabled = false
    write_capacity = 1
    attribute {
        name = "question_id"
        type = "S"
    }
    point_in_time_recovery {
        enabled = false
    }
}
