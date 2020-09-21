import requests
import json


def main(AUTH_CODE):

    # TODO add pickle saving (google example)
    # TODO add username/id string to token file name
    # TODO pickle file name should br Global on class build
    credantials = json.loads(
        open(r'social\linkedin_oauth2\credentials.json', 'rb').read())['web']

    ACCESS_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

    qd = {'grant_type': 'authorization_code',
          'code': AUTH_CODE,
          'redirect_uri': 'http://localhost:8080/linkedin/auth',
          'client_id': credantials['client_id'],
          'client_secret': credantials['client_secret']}

    response = requests.post(ACCESS_TOKEN_URL, data=qd, timeout=60)

    response = response.json()

    access_token = response['access_token']

    # TODO add username/id string to token file name
    open(r'social\linkedin_oauth2\tokens\token.json', 'w').write(
        json.dumps({"AccessToken": access_token,
                    "Expires": response['expires_in']})
    )
