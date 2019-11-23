from apis.helpers.utils import send_binary_api_requests


profile_id = '0e80af90-bede-4006-932b-c3b3a2f64994'

url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles/{}/enroll?".format(profile_id)

data_url = 'speaker_recognition/audios/recording_train.wav'
querystring = {}


def add_enrollment(recording):
    send_binary_api_requests(url, querystring, '24e9de72f0cc4a27a3d2b4afd43f755f', recording)


