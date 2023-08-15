from dotenv import load_dotenv # modulo para almancenar variables de ambiente de archivos .env
import os
import requests

load_dotenv() 

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')



