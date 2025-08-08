# Define S3 bucket resource


#makes sure the S3 bucket has a unqiue name
resource "random_string" "bucket_suffix" {
    length = 8
    special = false
    upper = false
}

#creates the bucket
resource "aws_s3_bucket" "raw_music_data" {
    bucket = "music-trends-data-lake-${random_string.bucket_suffix.result}"
    tags = {
        Name = "Music Trends Data Lake"
        Project = "Spotify Stock Market"
    }
    
}

resource "aws_s3_bucket_public_access_block" "raw_artist_data_access" {
    bucket = aws_s3_bucket.raw_music_data.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}