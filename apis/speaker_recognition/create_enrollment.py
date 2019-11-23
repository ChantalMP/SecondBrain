from apis.helpers.utils import send_binary_api_requests

def add_enrollment(recording, profile_id):
    querystring = {}
    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles/{}/enroll?".format(profile_id)
    send_binary_api_requests(url, querystring, '24e9de72f0cc4a27a3d2b4afd43f755f', recording)

#add_enrollment("apis/speaker_recognition/audios/marcel.wav","c442f831-f76f-4184-ab95-559757354976") #marcel
#add_enrollment("apis/speaker_recognition/audios/ege.wav","8cf2b837-478a-4876-8ff4-9a59683c0869") #ege
#add_enrollment("apis/speaker_recognition/audios/michi.wav","5ddf4737-568d-4970-a116-9c01032fd1ea") #michi
#add_enrollment("apis/speaker_recognition/audios/talle.wav","64e3fae5-987e-4dcd-84fe-efc36f4d2ef2") #chantal