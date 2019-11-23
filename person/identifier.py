import apis.speaker_recognition.identify as identify_speech
import apis.face_api.identify as identify_face
import json

def identify_by_speech(recording):
    text = identify_speech.identify(recording)
    return json.loads(text)["processingResult"]["identifiedProfileId"]

def identify_by_image(image):
    identify_face.identify(image)

def identify_by_tag(tag):
    pass

identify_by_image("apis/face_api/images/talle_test.jpg")