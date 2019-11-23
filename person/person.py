import apis.face_api.detect as face_detect
import apis.speaker_recognition.create_profile as create_profile
import apis.speaker_recognition.create_enrollment as create_enrollment

class Person:
    person_id = 0
    speech_id = 0
    image_id = 0
    image = None
    tags = []
    name = ""
    address = ""
    phone = 0

    def __init__(self, recording, image, tags, name, address, phone):
        self.image = image
        self.tags = tags
        self.name = name
        self.address = address
        self.phone = phone

        self.image_id = face_detect.get_person_id(image)
        self.speech_id = create_profile.create_person()
        create_enrollment.add_enrollment(recording)

    def to_string(self):
        string = "person_id: {}\n \
                 speech_id: {} \n \
                 image_id: {} \n \
                 tags: {} \n \
                 name: {}\n ".format(self.person_id, self.speech_id, self.image_id, self.tags,self.name)
        return string


p = Person(recording='apis/speaker_recognition/audios/recording_testing.wav',\
           image='apis/face_api/images/IMG_2629.jpg',\
           tags=["Mum"],\
           name="dummy_name",\
           address="dummy-add",\
           phone=1234567)

print(p.to_string())


