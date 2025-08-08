# defeine the aws_lambda_function resource


# resource "archive_file" "daily_trigger_package" {
#   type = "zip"
#   source_file = "${path.module}/lambda_code/daily_collector.py"
#   output_path = "${path.module}/lambda_code/function.zip"
# }

resource "aws_lambda_function" "weekly_discog_checker" {
  function_name = "weekly-worker-function"
  role = aws_iam_role.lambda_iam_role.arn

  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.raw_music_data.bucket
    #   BUCKET_NAME = aws_s3_bucket.raw_music_data.bucket
      SPOTIFY_CLIENT_ID = var.spotify_client_id
      SPOTIFY_CLIENT_SECRET = var.spotify_client_secret
    }
  }


  filename = "${path.module}/discography_function.zip"

  #the hash tells TF to re-upload the zip file when the code changes
  source_code_hash = filebase64sha256("${path.module}/discography_function.zip")

  #handler = entry point in the code
  handler = "get_discography.lambda_handler"

  runtime = "python3.11"

  timeout = 900
  memory_size = 512

  tags = {
    Project = "Spotify Stock Market"
  }
}