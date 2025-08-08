

import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

#globals
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
SP_CLIENT = spotipy.Spotify(auth_manager=auth_manager, retries=5, status_retries=5, backoff_factor=0.3)
S3_CLIENT = boto3.client('s3')


def lambda_handler(event, context):
    
    BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

    #Load the list of artist IDs to track
    with open('unique_artist_ids.json', 'r') as f:
        artist_ids = json.load(f)
        artist_ids = [id for id in artist_ids if id]

    
    previous_releases = set()
    s3_state_file_key = "raw/release-history/all_discography_data.jsonl"
    try:
        response = S3_CLIENT.get_object(Bucket=BUCKET_NAME, Key=s3_state_file_key)
        previous_data = [json.loads(line) for line in response['Body'].read().decode('utf-8').splitlines()]
        previous_releases = {album['album_id'] for album in previous_data}
        print(f"Loaded {len(previous_releases)} previous releases from state file.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print("No state file found. Starting fresh.")
        else:
            raise e
            
    # get the CURRENT full discography from Spotify
    current_releases_list = []
    total_artists = len(artist_ids)
    print(f"Starting to fetch discographies for {total_artists} artists...")

    for i, artist_id in enumerate(artist_ids):
        print(f"Processing artist {i + 1}/{total_artists} (ID: {artist_id})")
        offset = 0
        limit = 50
        while True:
            try:
                results = SP_CLIENT.artist_albums(artist_id, limit=limit, offset=offset)
                for album in results['items']:
                    current_releases_list.append({
                        'artist_id': artist_id,
                        'album_id': album['id'],
                        'album_name': album['name'],
                        'album_type': album['album_type'],
                        'release_date': album['release_date'],
                        'total_tracks': album['total_tracks']
                    })
                
                if results['next']:
                    offset += limit
                else:
                    break
            except Exception as e:
                print(f"  An error occurred for artist {artist_id}: {e}")
                break


    #Compare and find new releases
    current_release_ids = {album['album_id'] for album in current_releases_list}
    new_release_ids = current_release_ids.difference(previous_releases)
    newly_discovered_releases = [album for album in current_releases_list if album['album_id'] in new_release_ids]
    print(f"Found {len(newly_discovered_releases)} new releases.")

    #Save outputs back to S3 
    if current_releases_list:
        # Group the full discography and save as PARTITIONED files for Athena
        grouped_releases = {}
        for release in current_releases_list:
            try:
                date_parts = release['release_date'].split('-')
                year = date_parts[0]
                month = date_parts[1] if len(date_parts) > 1 else '01'
                
                key = (year, month)
                if key not in grouped_releases:
                    grouped_releases[key] = []
                grouped_releases[key].append(release)
            except IndexError:
                print(f"Skipping release with malformed date: {release.get('release_date')}")

        
        for (year, month), releases_in_group in grouped_releases.items():
            s3_partition_key = f"raw/release-history/release_year={year}/release_month={month}/releases.jsonl"
            output_body = '\n'.join([json.dumps(record) for record in releases_in_group])
            S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=s3_partition_key, Body=output_body)
        
        #Overwrite the single STATE FILE with the complete current list for the next run
        S3_CLIENT.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_state_file_key,
            Body='\n'.join([json.dumps(record) for record in current_releases_list])
        )
        
        #If new releases were found, save them to a separate file for easy access
        if newly_discovered_releases:
            today_date = datetime.utcnow().strftime("%Y-%m-%d")
            s3_new_releases_key = f"processed/new-releases/{today_date}-new-releases.jsonl"
            S3_CLIENT.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_new_releases_key,
                Body='\n'.join([json.dumps(record) for record in newly_discovered_releases])
            )
            print(f"Saved new releases to {s3_new_releases_key}")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Found {len(newly_discovered_releases)} new releases.")
    }


