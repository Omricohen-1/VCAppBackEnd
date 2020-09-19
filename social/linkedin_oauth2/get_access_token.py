import requests
import json


def main(AUTH_CODE):
    credantials = json.loads(
        open(r'social\linkedin_oauth2\credentials.json', 'rb').read())['web']

    ACCESS_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

    qd = {'grant_type': 'authorization_code',
        'code': AUTH_CODE,
        'redirect_uri': 'http://localhost:8080/linkedin_auth',
        'client_id': credantials['client_id'],
        'client_secret': credantials['client_secret']}

    response = requests.post(ACCESS_TOKEN_URL, data=qd, timeout=60)

    response = response.json()

    access_token = response['access_token']

    print ("Access Token:", access_token)
    print ("Expires in (seconds):", response['expires_in'])

