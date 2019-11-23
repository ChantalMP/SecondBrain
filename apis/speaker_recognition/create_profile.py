from apis.helpers.utils import send_json_post_api_requests

import json

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"

payload = ('{\n"locale":"en-us"}')


def create_person():
    _,text = send_json_post_api_requests(url, {}, '24e9de72f0cc4a27a3d2b4afd43f755f', payload)
    return json.loads(text)['identificationProfileId']

#id_marcel = create_person() #c442f831-f76f-4184-ab95-559757354976
#id_chantal = create_person() #64e3fae5-987e-4dcd-84fe-efc36f4d2ef2
#id_ege = create_person() #8cf2b837-478a-4876-8ff4-9a59683c0869
#id_michi = create_person() #5ddf4737-568d-4970-a116-9c01032fd1ea
