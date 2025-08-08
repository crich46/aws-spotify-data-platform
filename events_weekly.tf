# define the EventBridge rule and target

# configure to run my Lambda function once a day

resource "aws_cloudwatch_event_rule" "trigger_lambda_weekly" {
    name = "trigger-lambda-weekly"
    description = "This function needs to trigger my lambda function once a week to gather artist data"

    schedule_expression = "cron(0 8 ? * FRI *)"
}


#connects rule to the target
resource "aws_cloudwatch_event_target" "weekly_trigger_cloudwatch_connect" {
    rule = aws_cloudwatch_event_rule.trigger_lambda_weekly.name
    
    #arn has to be the arn of the target; the lambda function
    arn = aws_lambda_function.weekly_discog_checker.arn
  
}

resource "aws_lambda_permission" "allow_cloudwatch_weekly" {
    statement_id = "AllowExecutionFromCloudWatchWeekly"
    action = "lambda:InvokeFunction"
    principal = "events.amazonaws.com"
    function_name = aws_lambda_function.weekly_discog_checker.function_name

    #link back to the specific rule that is allowed to trigger the function
    source_arn = aws_cloudwatch_event_rule.trigger_lambda_weekly.arn
}