
import json
import requests
import string
import random

def main():
    credantials = json.loads(
        open(r'social\linkedin_oauth2\credentials.json', 'rb').read())['web']

    # TODO add username/id string to token file name
    # TODO pickle file name should br Global on class build
    # TODO add pickle saving (google example)

    # Copy the client ID, secret, and redirect URI in the fields below
    CLIENT_ID    = credantials['client_id']
    CLIENT_SECRET = credantials['client_secret']
    REDIRECT_URI = 'http://localhost:8080/linkedin_auth'

    # Generate a random string to protect against cross-site request forgery
    letters = string.ascii_lowercase
    CSRF_TOKEN = ''.join(random.choice(letters) for i in range(24))


    # Request authentication URL
    auth_params = {'response_type': 'code',
                'client_id': CLIENT_ID,
                'redirect_uri': REDIRECT_URI,
                'state': CSRF_TOKEN,
                'scope': 'r_liteprofile r_emailaddress'}

    html = requests.get("https://www.linkedin.com/oauth/v2/authorization",
                        params = auth_params)

    # Print the link to the approval page
    print(html.url) #TODO launch the url

        # Click the link below to be taken to your redirect page.


if __name__ == '__main__':
    main()
