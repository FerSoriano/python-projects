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
        self.__error = ''
    
    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

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
        self.token = 'BQAPs2KrHpkGru9smoK9O6RX87c1kRPDx2xrT9rES01pCe27j5MaG_hcLBQ4cFeB8LeCp1vc5wgZAcOTXJgPc97w8zSyei0wRiDaLfBiQZ1lGjtIEpE'
    
    def getRequestResult(self, url, metodo = ''):
        result = requests.get(url=url,headers=self.__createAccessToken())
        
        if result.status_code == 403:
            print('Bad OAuth request.')
            self.__error = 403
            return self.__error
        
        json_result = json.loads(result.content)
        
        if metodo == 'id':
            try:
                if json_result['error']['status'] == 401:
                    print(json_result)
                    self.__error = 0 # Token expired
                    return self.__error
            except:
                if json_result['artists']['items'] == []:
                    print('Artista no encontrado.')
                    self.__error = 1 # Artist not found
                    return self.__error
                
        return json_result

    def __createAccessToken(self):
        return {'Authorization': 'Bearer ' + self.token}    

    def __getArtistID(self, artist_name):
        url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'

        result = self.getRequestResult(url,'id')

        if self.__error == 0 or self.__error == 1:
            exit()

        artistID = result['artists']['items'][0]['id']
        self.artist_name = result['artists']['items'][0]['name']
        
        return artistID
    
    def getArtistSongs(self, artist_name):
        url = f'https://api.spotify.com/v1/artists/{self.__getArtistID(artist_name)}/top-tracks?market=MX'
        
        result = self.getRequestResult(url)
        
        songs = result['tracks']


        print(f'TOP CANCIONES: {self.artist_name}')

        for i, song in enumerate(songs):
            print(f'{i + 1}. {song["name"]}')


from flask import Flask




class Spotify_User(API_Spotify):
    def __init__(self, client_id, client_secret, user_name):
        super().__init__(client_id, client_secret)
        self.user_name = user_name

#TODO: Ver al autorizacion OAuth 2.0

   
    # app = Flask(__name__)
    # app.run()
    # @app.route('/')
    # def login():
    #     return 'Hola'
    

    def getOAuth(self):
        redirect_uri = 'http://127.0.0.1:5000/'
        scope = 'user-read-private user-read-email'

        url = f'https://accounts.spotify.com/authorize?response_type=token&client_id={self.client_id}&scope={scope}&redirect_uri={redirect_uri}'

        result = requests.post(url=url)
        print(result)
        # json_result = json.loads(result.content)
        # print(json_result)


# TODO: Terminar metodo
    def get_user_playlist(self):
        url = 'https://api.spotify.com/v1/me/playlists'
        return
    
        # Get the current user's top artists or tracks based on calculated affinity.
    def getUsersTopItems(self, item_type = "artists", time_range = "short_term"):
        """
        item_type = "artists" or "tracks"
        long_term = all the time (almost)
        medium_term = last 6 months
        short_term = last 4 weeks
        """
        terms = ['long_term', 'medium_term', 'short_term']
        if not time_range in terms:
            print('Rango de tiempo no valido.')
            exit()
        url = f'https://api.spotify.com/v1/me/top/{item_type}?time_range={time_range}'

        result = self.getRequestResult(url)
        if result == 403:
            exit()
        
        artists = result['name']
        print(artists)




user = Spotify_User(client_id, client_secret, 'feersoriano')
# print(user.getToken())
user.getTokenTemp()
# user.getArtistSongs('alvvays')
user.getUsersTopItems()
# user.getOAuth()
# user.getUsersTopItems('artists','short_term')

