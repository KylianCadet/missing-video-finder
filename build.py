from dotenv import load_dotenv
import os

load_dotenv('.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_KEY = os.getenv('API_KEY')

keys = {
    'CLIENT_ID': CLIENT_ID,
    'CLIENT_SECRET': CLIENT_SECRET,
    'API_KEY': API_KEY
}

s = ""
for key, val in keys.items():
    s += key
    s += '=\''
    s += val
    s += '\'\n'

credentials_file = open('./missing_video_finder/credentials.py', 'r+')
credentials_content = credentials_file.read()
credentials_file.seek(0)
credentials_file.write(s)
credentials_file.truncate()
credentials_file.close()

os.system("pyinstaller --onefile --icon=data/img/icon.png --noconsole cli.spec")

credentials_file = open('./missing_video_finder/credentials.py', 'w+')
credentials_file.seek(0)
credentials_file.write(credentials_content)
credentials_file.truncate()
credentials_file.close()