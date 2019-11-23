from apis.helpers.utils import send_binary_api_requests,send_json_get_api_requests
from time import sleep

import json

profile_ids = '0e80af90-bede-4006-932b-c3b3a2f64994'

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identify?identificationProfileIds={}&shortAudio=true".format(
    profile_ids)


def identify(recording):

    header = send_binary_api_requests(url, {}, '24e9de72f0cc4a27a3d2b4afd43f755f', recording)
    operation_location = header[0]['Operation-Location']
    timeout = 20
    while timeout >= 0:
        timeout -= 1
        sleep(1)
        _, text = send_json_get_api_requests(operation_location, {}, '24e9de72f0cc4a27a3d2b4afd43f755f')
        status = json.loads(text)['status']
        if status == 'succeeded':
            return text
