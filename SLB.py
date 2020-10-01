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

# All tracks requisition
# Maybe it can be improved using threads and/or generators and list comprehension
i = 0
tracks = spotify.saved_tracks(market=None, limit=50, offset=i)
songs = tracks.items
while len(tracks.items) > 0:
    i += 50
    print("Músicas coletadas: ", i)
    tracks = spotify.saved_tracks(market=None, limit=50, offset=i)
    songs.extend(tracks.items)

songs.sort(key = lambda x: (
    unidecode.unidecode(x.track.album.artists[0].name.lower()), 
    unidecode.unidecode(x.track.album.name.lower()),
    x.track.disc_number, 
    x.track.track_number
))

# Saving to the file
with open("songs.txt", "w+") as f:
    for song in songs:
        line = f"{song.track.album.artists[0].name} - {song.track.album.name} - {song.track.track_number} - {song.track.name}\n"
        f.write(line)
