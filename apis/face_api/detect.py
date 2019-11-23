from apis.helpers.utils import send_binary_api_requests

import json

url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"

image = 'apis/face_api/images/IMG_2630.jpg'

querystring = {"returnFaceId": "true", "returnFaceLandmarks": "false", "recognitionModel": "recognition_02", "returnRecognitionModel": "True",
               "detectionModel": "detection_01"}

key = '15262392d8164ba3bb431da6b0c11f42'


def get_person_id(image):
    _, text = send_binary_api_requests(url, querystring, key, image)
    return json.loads(text)[0]['faceId']
