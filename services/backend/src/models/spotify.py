import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyWrapper:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public playlist-read-private"
        ))

    def getPlayListByName(self, playlist_name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist
        return None

    def createPlaylist(self, playlist_name):
        user_id = self.sp.current_user()['id']
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        return playlist

    def addSongToPlaylist(self, playlist_id, song_name, artist_name):
        query = f"track:{song_name} artist:{artist_name}"
        results = self.sp.search(query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])

        if not tracks:
            return

        track_id = tracks[0]['id']
        self.sp.playlist_add_items(playlist_id, [track_id])

    def ensurePlaylistWithSong(self, playlist_name, song_name, artist_name):
        playlist = self.getPlayListByName(playlist_name)

        if playlist is None:
            playlist = self.createPlaylist(playlist_name)

        self.addSongToPlaylist(playlist['id'], song_name, artist_name)