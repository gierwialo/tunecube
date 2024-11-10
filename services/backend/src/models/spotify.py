import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyWrapper:
    def __init__(self, client_id, client_secret, redirect_uri, scope, token_file_path='token.json', refresh_file_path='refresh.json'):
        self.sp_oauth = SpotifyOAuth(client_id=client_id,
                                     client_secret=client_secret,
                                     redirect_uri=redirect_uri,
                                     scope=scope)
        self.sp = None
        self.token_file_path = token_file_path
        self.refresh_file_path = refresh_file_path

    def getAuthorizeUrl(self):
        return self.sp_oauth.get_authorize_url()

    def getAccessToken(self, code):
        token_info = self.sp_oauth.get_access_token(code)
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        return token_info

    def refreshAccessToken(self, refresh_token):
        token_info = self.sp_oauth.refresh_access_token(refresh_token)
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        return token_info

    def setClientFromToken(self, token_info):
        self.sp = spotipy.Spotify(auth=token_info['access_token'])

    def saveTokenToFile(self, token_info):
        with open(self.token_file_path, 'w') as token_file:
            json.dump(token_info, token_file)
        with open(self.refresh_file_path, 'w') as refresh_file:
            json.dump({'refresh_token': token_info['refresh_token']}, refresh_file)

    def loadTokenFromFile(self):
        if os.path.exists(self.token_file_path):         
            if os.path.getsize(self.token_file_path) == 0:
                return None

            with open(self.token_file_path, 'r') as token_file:
                try:
                    return json.load(token_file)
                except json.JSONDecodeError:
                    return None

        elif os.path.exists(self.refresh_file_path):
            if os.path.getsize(self.refresh_file_path) == 0:
                return None

            with open(self.refresh_file_path, 'r') as refresh_file:
                try:
                    refresh_info = json.load(refresh_file)
                except json.JSONDecodeError:
                    return None

                if self.sp_oauth.is_token_expired(refresh_info):
                    token_info = self.refreshAccessToken(refresh_info['refresh_token'])
                    self.save_token_to_file(token_info)
                    return token_info
        return None

    def getPlayListByName(self, playlist_name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist
        return None

    def getPlaylistUrlByName(self, playlist_name):
        playlist = self.getPlayListByName(playlist_name)
        if playlist:
            return playlist['external_urls']['spotify']
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