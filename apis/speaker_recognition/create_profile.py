from apis.helpers.utils import send_json_post_api_requests

import json

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"

payload = ('{\n"locale":"en-us"}')


def create_person():
    _,text = send_json_post_api_requests(url, {}, '24e9de72f0cc4a27a3d2b4afd43f755f', payload)
    return json.loads(text)['identificationProfileId']
