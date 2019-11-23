from apis.helpers.utils import send_binary_api_requests,send_json_get_api_requests
from time import sleep

import json

profile_ids = 'c442f831-f76f-4184-ab95-559757354976,64e3fae5-987e-4dcd-84fe-efc36f4d2ef2,8cf2b837-478a-4876-8ff4-9a59683c0869,5ddf4737-568d-4970-a116-9c01032fd1ea'

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identify?identificationProfileIds={}&shortAudio=true".format(
    profile_ids)


def identify(recording):

    header = send_binary_api_requests(url, {}, '24e9de72f0cc4a27a3d2b4afd43f755f', recording)
    operation_loceditation = header[0]['Operation-Location']
    timeout = 20
    querystring = r'{"identificationProfileIds:"}'+profile_ids
    while timeout >= 0:
        timeout -= 1
        sleep(1)
        _, text = send_json_get_api_requests(operation_location, querystring, '24e9de72f0cc4a27a3d2b4afd43f755f')
        status = json.loads(text)['status']
        if status == 'succeeded':
            return text
