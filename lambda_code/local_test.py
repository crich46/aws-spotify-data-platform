import os
from dotenv import load_dotenv
from unittest.mock import patch

load_dotenv()

# The @patch decorator temporarily replaces the real S3 call with our fake one
@patch('boto3.client')
def run_test(mock_boto3_client):
    # Configure the mock to behave like the real S3 client
    mock_s3 = mock_boto3_client.return_value
    
    # Import the handler AFTER the patch is active
    import daily_collector

    print("Executing lambda_handler with MOCKED S3 client...")
    response = daily_collector.lambda_handler(event={}, context={})
    
    # Check that the put_object method was called
    assert mock_s3.put_object.called, "S3 client's put_object was NOT called!"
    
    # Print the arguments that were passed to put_object
    print("\n--- S3 put_object was called with: ---")
    print(mock_s3.put_object.call_args)
    print("\n--- Lambda Response ---")
    print(response)

if __name__ == "__main__":
    run_test()