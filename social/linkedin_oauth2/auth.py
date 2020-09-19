
from linkedin_v2 import linkedin
import json


def main():
    credantials = json.loads(
        open(r'social\linkedin_oauth2\credentials.json', 'rb').read())['web']

    # TODO add username/id string to token file name
    # TODO pickle file name should br Global on class build
    # TODO add pickle saving (google example)

    # Define CONSUMER_KEY, CONSUMER_SECRET,
    # USER_TOKEN, and USER_SECRET from the credentials
    # provided in your LinkedIn application

    # Instantiate the developer authentication class
    # API_TOKEN = credantials['api_token']
    API_KEY = 'wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl'
    API_SECRET = 'daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG'
    RETURN_URL = 'http://localhost:8000'

    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
    # Optionally one can send custom "state" value that will be returned from OAuth server
    # It can be used to track your user state or something else (it's up to you)
    # Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
    #authorization.state = 'your_encoded_message'
    print (authentication.authorization_url)  # open this url on your browser
    application = linkedin.LinkedInApplication(authentication)


if __name__ == '__main__':
    main()
