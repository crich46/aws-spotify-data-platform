import os
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
import json
from botocore.exceptions import ClientError

# Load local environment variables from .env file
load_dotenv()

# The @patch decorator replaces the real boto3.client with our mock
@patch('boto3.client')
def run_test(mock_boto3_client):
    # Configure the mock S3 client
    mock_s3 = MagicMock()
    
    # --- SCENARIO 1: Simulate the first-ever run (file not in S3) ---
    print("--- Running Test: First-Time Execution ---")
    # Make the mock 'get_object' raise a "NoSuchKey" error
    mock_s3.get_object.side_effect = ClientError(
        error_response={'Error': {'Code': 'NoSuchKey'}},
        operation_name='GetObject'
    )
    mock_boto3_client.return_value = mock_s3
    
    # Import the handler AFTER the patch is active
    import get_discography

    # Run the handler
    response = get_discography.lambda_handler({}, {})
    
    # Check that put_object was called to save the new discography
    assert mock_s3.put_object.called, "S3 put_object was NOT called!"
    print("✅ Test Passed: S3 put_object was called as expected.\n")


    # --- SCENARIO 2: Simulate a subsequent run (file exists in S3) ---
    print("--- Running Test: Subsequent Execution ---")
    # Reset the mock for the new test
    mock_s3.reset_mock()
    
    # Make the mock 'get_object' return a fake previous file
    fake_previous_data = [{'album_id': 'old_album_123'}]
    mock_s3.get_object.side_effect = None # Remove the error side_effect
    mock_s3.get_object.return_value = {
        'Body': MagicMock(read=lambda: json.dumps(fake_previous_data).encode('utf-8'))
    }
    
    response = get_discography.lambda_handler({}, {})
    
    assert mock_s3.put_object.called, "S3 put_object was NOT called!"
    print("✅ Test Passed: Loaded previous data and saved new data.")


if __name__ == "__main__":
    run_test()

416 