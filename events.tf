# define the EventBridge rule and target

# configure to run my Lambda function once a day

resource "aws_cloudwatch_event_rule" "trigger_lambda_daily" {
    name = "trigger-lambda-daily"
    description = "This function needs to trigger my lambda function daily to gather artist data"

    schedule_expression = "cron(0 12 * * ? *)" #this should run at 12:00pm UTC every day
}


#connects rule to the target
resource "aws_cloudwatch_event_target" "daily_trigger_cloudwatch_connect" {
    rule = aws_cloudwatch_event_rule.trigger_lambda_daily.name
    
    #arn has to be the arn of the target; the lambda function
    arn = aws_lambda_function.daily_trigger.arn


  
}

resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    principal = "events.amazonaws.com"
    function_name = aws_lambda_function.daily_trigger.function_name

    #link back to the specific rule that is allowed to trigger the function
    source_arn = aws_cloudwatch_event_rule.trigger_lambda_daily.arn
}