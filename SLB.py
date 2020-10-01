import os
import tekore as tk
import unidecode

# Authentication
client_id = 'ClientIDHere'
client_secret = 'ClientSecretHere'
app_token = tk.request_client_token(client_id, client_secret)
spotify = tk.Spotify(app_token)
redirect_uri = 'http://localhost:8888/callback'
spotify.token = tk.prompt_for_user_token(
    client_id,
    client_secret,
    redirect_uri,
    scope=tk.scope.every
)
os.system('clear')

# Will get BATCH_SIZE songs per request
BATCH_SIZE = 50

# All tracks requisition
songs = []
while True:
    print(f'Coletando músicas... Total: {len(songs)}')
    tracks = spotify.saved_tracks(market=None, limit=BATCH_SIZE, offset=len(songs))
    if not tracks or not tracks.items:
        break

    songs.extend(tracks.items)

songs.sort(key = lambda x: (
    unidecode.unidecode(x.track.album.artists[0].name.lower()), 
    unidecode.unidecode(x.track.album.name.lower()),
    x.track.disc_number, 
    x.track.track_number
))

# Saving to the file
with open('songs.txt', 'w+') as f:
    for song in songs:
        line = f"{song.track.album.artists[0].name} - {song.track.album.name} - {song.track.track_number} - {song.track.name}\n"
        f.write(line)