#This is the code that terraform zips and deploys to AWS Lambda

#Read the list of IDs from the ARTIST_IDS.json file.

import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import boto3
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
SP_CLIENT = spotipy.Spotify(auth_manager=auth, retries=5, status_retries=5, backoff_factor=0.3)
S3_CLIENT = boto3.client('s3')

# Read the list of IDs from the unique_artist_ids.json file.



def lambda_handler(event, context):
    with open('unique_artist_ids.json', 'r') as f:
        ARTIST_IDS = json.load(f)
        ARTIST_IDS = [id for id in ARTIST_IDS if id]
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    timestamp = datetime.utcnow().isoformat()
    
    #Batch the artist IDs into groups of 50
    batches = [ARTIST_IDS[i:i + 50] for i in range(0, len(ARTIST_IDS), 50)]
    
    # Print the batches.
    # print("\nBatches of 50 Artist IDs:")
    # for i, b in enumerate(batch):
    #     print(f"Batch {i + 1}, length {len(b)}:")
    #     for artist_id in b:
    #         print(artist_id)
    #     print()  # Print a newline for better readability
        
    # Process each batch and get the artist details
    # Get artist id, name, followers, genres, popularity, followers, and retrieved_at data
    all_artist_data = []
    for batch in batches:
        results = SP_CLIENT.artists(batch) # Always use sp.artists()
        
        for artist in results['artists']:
            if artist:
                all_artist_data.append({
                    'id': artist['id'],
                    'name': artist['name'],
                    'followers': artist['followers']['total'],
                    'genres': artist['genres'],
                    'popularity': artist['popularity'],
                    'retrieved_at': timestamp
                })

    # Save all artist data to S3
    output_body = '\n'.join([json.dumps(record) for record in all_artist_data])
    
    # Create S3 file key
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    s3_key = f"raw/daily-metrics/date={today_date}/metrics.jsonl"
    
    #Upload the file
    S3_CLIENT.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=output_body,
    )
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully processed {len(all_artist_data)} artists.')
    }