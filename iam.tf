# define IAM role and any related policies

# only give lambda function access to to what it absolutely needs

resource "aws_iam_role" "lambda_iam_role" {
  name = "music-trends-lambda-role"  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
            Service = "lambda.amazonaws.com"
        }
    }]
  })
  tags = {
    Project = "Spotify Stock Market"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
    role = aws_iam_role.lambda_iam_role.name
    policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

#this attachement is for basic lambda logging
resource "aws_iam_role_policy_attachment" "lambda_iam_attach" {
    role = aws_iam_role.lambda_iam_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"


}

data "aws_iam_policy_document" "s3_access_policy" {
    statement {
      effect = "Allow"
      actions = ["s3:PutObject", "s3:GetObject"]
      #bucket's arn string, including a wildcard for the objects
      resources = ["${aws_s3_bucket.raw_music_data.arn}/*"]
    }
    statement {
      effect = "Allow"
      actions = ["s3:ListBucket", "s3:GetObject"]
      resources = [aws_s3_bucket.raw_music_data.arn]
    }
}

#create custom IAM policy from document
resource "aws_iam_policy" "lambda_s3_policy" {
    name = "lambda-s3-put-object-policy"
    policy = data.aws_iam_policy_document.s3_access_policy.json

    tags = {
      Project = "Spotify Stock Market"
    }
}
