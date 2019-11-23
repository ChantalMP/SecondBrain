from apis.helpers.utils import send_binary_api_requests,send_json_get_api_requests
from time import sleep

import json

from secondBrainBackend.models import Person

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identify?identificationProfileIds={}&shortAudio=true"


def identify(recording):

    profile_ids = ','.join([elem["speech_id"] for elem in Person.objects.filter(speech_id__isnull=False).values("speech_id")])
    header = send_binary_api_requests(url.format(profile_ids), {}, '24e9de72f0cc4a27a3d2b4afd43f755f', recording)
    print(header)
    operation_location = header[0]['Operation-Location']
    timeout = 20
    querystring = r'{"identificationProfileIds:"}'+profile_ids
    while timeout >= 0:
        timeout -= 1
        sleep(1)
        _, text = send_json_get_api_requests(operation_location, querystring, '24e9de72f0cc4a27a3d2b4afd43f755f')
        status = json.loads(text)['status']
        print(text)
        if status == 'succeeded':
            return text
