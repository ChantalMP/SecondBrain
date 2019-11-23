import apis.speaker_recognition.identify as identify
import json

def identify_by_speech(recording):
    text = identify.identify(recording)
    return json.loads(text)["processingResult"]["identifiedProfileId"]

def identify_by_image(image):
    pass

def identify_by_tag(tag):
    pass

identify_by_speech('apis/speaker_recognition/audios/recording_testing.wav')
