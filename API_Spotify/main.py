from dotenv import load_dotenv # modulo para almancenar variables de ambiente de archivos .env
import os
import base64
import requests
import json

load_dotenv() 

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


class API_Spotify():
    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
    
    def getToken(self):
        auth_str = str(self.__client_id + ':' + self.__client_secret).encode('utf-8')
        auth_b64 = str(base64.b64encode(auth_str),encoding='utf-8')

        url = 'https://accounts.spotify.com/api/token'

        headers = {
            'Authorization': 'Basic ' + auth_b64
        }
        
        form = {
            'grant_type': 'client_credentials'
        }

        result = requests.post(url=url,data=form,headers=headers)
        json_result = json.loads(result.content)
        self.token = json_result['access_token']

        return self.token

    def getTokenTemp(self):
        self.token = 'BQD2IwLO14rdcb1lPoSH8KG6pGnE9uvT_lQyIqwOYX5lVgI7_p2uKxwCvspo0b7imEKn9u2BCmHD-8QLXphLN8W72aW6wkL-1z6N1eLEWTzv2kJF46A'
    
    def __getResult(self, url):
        result = requests.get(url=url,headers=self.__createAccessToken())
        json_result = json.loads(result.content)
        
        try:
            if json_result['error']['status'] == 401:
                print(json_result)
                exit()
        except:
            if json_result['artists']['items'] == []:
                print('Artista no encontrado.')
                exit()
        finally:
            return json_result

    def __createAccessToken(self):
        return {'Authorization': 'Bearer ' + self.token}

    def __getArtistID(self, artist_name):
        url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'

        result = self.__getResult(url)

        artistID = result['artists']['items'][0]['id']
        self.artist_name = result['artists']['items'][0]['name']
        
        return artistID
    
    def getArtistSongs(self, artist_name):
        url = f'https://api.spotify.com/v1/artists/{self.__getArtistID(artist_name)}/top-tracks?market=MX'
        
        result = self.__getResult(url)
        
        songs = result['tracks']


        print(f'TOP CANCIONES: {self.artist_name}')

        for i, song in enumerate(songs):
            print(f'{i + 1}. {song["name"]}')


# TODO: Analizar si crear una sub clase para obtener los datos de usuario -> Playlist, Canciones mas reproducidas, etc.
# TODO: Terminar metodo / Ver al autorizacion OAuth 2.0
    def get_user_playlist(self):
        url = 'https://api.spotify.com/v1/me/playlists'
        return
        

spotify = API_Spotify(client_id,client_secret)
# print(spotify.getToken())
spotify.getTokenTemp() 
spotify.getArtistSongs('Tame Impala')


