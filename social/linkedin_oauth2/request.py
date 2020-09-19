import requests
import json

access_token = json.loads(open(r'social\linkedin_oauth2\tokens\token.json','rb').read())['AccessToken']
params = {'oauth2_access_token': access_token,
          'fields': ["localizedFirstName,localizedLastName,id"]}
response = requests.get('https://api.linkedin.com/v2/me', params = params)

print(json.dumps(response.json(), indent=1))