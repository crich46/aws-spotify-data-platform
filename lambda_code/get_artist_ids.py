import spotipy
import json
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from dotenv import load_dotenv
load_dotenv()

# Functions
def read_tfvars(path):
    creds = {}
    with open(path) as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                creds[key.strip()] = value.strip().strip('"')
    return creds

def find_artist_ids(artist_names, sp_client):
    """
    Searches for a list of artist names and returns a dictionary of {name: id}.
    """
    artist_ids = {}
    # print("Searching for artist IDs...")
    
    for name in artist_names:
        # Use the 'artist' field filter for a more precise search
        results = sp_client.search(q=f"artist:{name}", type="artist", limit=1)
        
        items = results['artists']['items']
        if items:
            # If a result is found, grab the ID from the first item
            artist = items[0]
            artist_ids[name] = artist['id']
            # print(f"  Found: '{name}' -> ID: {artist['id']}")
        else:
            # Handle cases where no artist was found
            artist_ids[name] = None
            print(f"  Could not find ID for '{name}'")
            
    return artist_ids

def get_unique_artist_ids_from_playlist(playlist_uri, sp_client):
    """
    Gets the unique artist IDs from a given Spotify playlist URI.

    Args:
        playlist_uri (str): The URI of the Spotify playlist (e.g., 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M').
    Returns:
        set: A set containing unique artist IDs present in the playlist.
             Returns an empty set if the playlist is not found or an error occurs.
    """
    try:
        

        # Extract the playlist ID from the URI
        # URIs can be in the format 'spotify:playlist:ID' or 'https://open.spotify.com/playlist/ID?si=...'
        if "spotify:playlist:" in playlist_uri:
            playlist_id = playlist_uri.split(":")[-1]
        elif "open.spotify.com/playlist/" in playlist_uri:
            playlist_id = playlist_uri.split("/")[-1].split("?")[0]
        else:
            print(f"Error: Invalid playlist URI format: {playlist_uri}")
            return set()

        artist_ids = set()
        results = sp_client.playlist_items(playlist_id)
        tracks = results['items']

        # Spotify API returns 100 tracks at a time, so we need to paginate
        while results['next']:
            results = sp_client.next(results)
            tracks.extend(results['items'])

        for item in tracks:
            # Check if the item is a track (sometimes podcasts or local files might be in a playlist)
            if item and 'track' in item and item['track']:
                for artist in item['track']['artists']:
                    artist_ids.add(artist['id'])
        return artist_ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()


# Credential Setup

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
SP_CLIENT = spotipy.Spotify(auth_manager=auth)









# Tracks, Artist Names, and Playlist Gathering
results = SP_CLIENT.search(q = 'year:2025', type = 'track', market='US', limit=50)

playlist_uris = ['spotify:playlist:7EnIitpBIDp8hbqoaOWfQO', 'spotify:playlist:1TfBE6fgKlgk1xtpX7b91k', 'spotify:playlist:5HMZFHhU3lVv6FMQVoDIG6', 'spotify:playlist:5wenUIAuOHhRoIOvbSuuNr']
custom_additions = [
    'Quadeca',
    'Yeat',
    'Jane Remover',
    'ericdoa',
    'osamason',
    'Ken Carson',
    'Playboi Carti',
    'Kendrick Lamar',
    'Panic! At the Disco',
    'Dev Lemons',
    'JID',
    '2hollis',
    'Ski Mask the Slump God',
    'Lil Uzi Vert',
    'Lil Yachty',
    'Lil Keed',
    'Lil Baby',
    'Lil Durk',
    'Lil Wayne',
    'Lil Nas X',
    'Lil Peep',
    'Lil Pump',
    'Lil Tracy',
    'Kenny Mason',
    'J Cole',
    'Travis Scott',
    'Tyler, The Creator',
    'Kanye West',
    'Drake',
    'SZA',
    'Doja Cat',
    'Billie Eilish',
    'Olivia Rodrigo',
    'The Weeknd',
    'Dua Lipa',
    'Ariana Grande',
    'Beyoncé',
    'Taylor Swift',
    'Ed Sheeran',
    'Justin Bieber',
    'Post Malone',
    'Harry Styles',
    'Sam Smith',
    'Halsey',
    'Shawn Mendes',
    'Camila Cabello',
    'Charlie Puth',
    'Maroon 5',
    'Imagine Dragons',
    'Coldplay',
    'OneRepublic',
    'Panic! At The Disco',
    'Twenty One Pilots',
    'Paramore',
    'Fall Out Boy'
]


# Artist ID Retrieval

# 1. Get unique artist IDs from the playlist
playlist_artists = set()
for uri in playlist_uris:
    # Pass the existing 'sp' object to your (modified) function
    ids_from_playlist = get_unique_artist_ids_from_playlist(uri, SP_CLIENT) 
    playlist_artists.update(ids_from_playlist)
print(f"Found {len(playlist_artists)} artists from playlists.")

# 2. Get artist IDs for custom additions
custom_artists = find_artist_ids(custom_additions, SP_CLIENT)
custom_artist_ids = {id for id in custom_artists.values() if id}
print(f"Found {len(custom_artist_ids)} artists from custom list.")

# 3. Get artist IDs for the top 50 tracks released in the current year
results = SP_CLIENT.search(q = 'year:2025', type = 'track', market='US', limit=50)
discovered_artists_ids = set()
for track in results['tracks']['items']:
    if track: # Add a check for None tracks
        for artist in track['artists']:
            discovered_artists_ids.add(artist['id'])
print(f"Found {len(discovered_artists_ids)} artists from top tracks search.")
# 4. Combine all unique artist IDs
all_unique_artists = playlist_artists.union(custom_artist_ids, discovered_artists_ids)

# 5. Print the total number of unique artists
print(f"\nTotal unique artists: {len(all_unique_artists)}")

# 6. Save the unique artist IDs to a JSON file
output_file = 'unique_artist_ids.json'
with open(output_file, 'w') as f:
    json.dump(list(all_unique_artists), f, indent=4)

print(f"Artist ID list saved to '{output_file}'")