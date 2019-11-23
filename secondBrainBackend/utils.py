from secondBrainBackend.models import Data, Information, Tag
from apis.image_tagging.image_tagging import get_tags_for_image
import apis.speaker_recognition.identify as identify_speech
import apis.face_api.identify as identify_face
import json

import numpy as np


def create_information(data: Data, tags=None):
    '''
    :param data: image,note,location
    '''
    information = Information.objects.create(data)
    for tag in tags:
        new_tag = Tag.objects.get_or_create(text=tag)
        information.tags.add(new_tag)

    # Call auto tagging
    information.get_additional_tags()
    return information


def find_matching_infos(tags, informations):
    '''

    :param tags: List [Tag]
    :param informations:
    :return:
    '''
    results = {}

    for information in informations:
        score = information.compare_tags(tags)
        results[information] = score

    sorted_results = sorted(results.items(), key=lambda kv: kv[1])

    return sorted_results[:3]


def process_input(raw_data, informations, data_type='tag'):
    '''
    :param raw_data: image_path or tag[s](seperated by comma)
    :return:
    '''
    if data_type == 'image':
        raw_tags = get_tags_for_image(raw_data)

    else:
        if ',' in raw_data:
            raw_tags = raw_data.split(',')
        else:
            raw_tags = [raw_data]

    tags = []
    for raw_tag in raw_tags:
        tag = Tag.objects.get_or_create()
        tags.append(tag)

    # here we should have tags
    find_matching_infos(tags, informations)


def identify_by_speech(recording):
    text = identify_speech.identify(recording)
    return json.loads(text)["processingResult"]["identifiedProfileId"]

def identify_by_image(image):
    identify_face.identify(image)

def identify_by_tag(tag):
    # TODO
    pass

def compare_tags(self, obj_tags):
    # TODO be careful, obj_tags are now django models
    # TODO create word embedding for these
    # TODO generate embeddings
    total_distance = 0.0
    count = 0.0

    self_embeddings = []
    obj_embeddings = []

    for self_embedding in self_embeddings:
        for obj_embedding in obj_embeddings:
            dist = np.linalg.norm(self_embedding - obj_embedding)
            total_distance += dist
            count += 1

    try:
        score = total_distance / count

    except Exception as e:
        return 100.0

    return score  # Smaller is better

# identify_by_image("apis/face_api/images/talle_test.jpg")

# if __name__ == '__main__':
#     from database import informations
#
#     note_data = NoteData('How does my dog look like? And how does my cat look like')
#     informations.append(create_information(note_data))
#
#     image_data = ImageData('apis/face_api/images/IMG_2629.jpg')
#     informations.append(create_information(image_data))
#
#     pickle.dump(informations, open("database/informations.p", "wb"))
#
#     tags = 'dog'
#     process_input(tags, informations)


#
# p = Person(recording='apis/speaker_recognition/audios/recording_testing.wav', \
#            image='apis/face_api/images/IMG_2629.jpg', \
#            tags=["Mum"], \
#            name="dummy_name", \
#            address="dummy-add", \
#            phone=1234567)
#
# print(p.to_string())