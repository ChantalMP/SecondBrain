from secondBrainBackend.models import Data, Information, Tag, Person
from apis.image_tagging.image_tagging import get_tags_for_image
import apis.speaker_recognition.identify as identify_speech
import apis.face_api.identify as identify_face
import json
import spacy

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


nlp = spacy.load("en_core_web_md")

def get_matching_information(tags, only_persons=False):

    results = {}

    tokens = nlp(' '.join(tags))

    if not only_persons:
        for information in Information.objects.all():
            information_tags = [elem.text for elem in information.tags.all()]
            information_tokens = nlp(' '.join(information_tags))
            total_similarity = 0.0
            count = 0.0

            for token in tokens:
                best_similarity = -1
                for information_token in information_tokens:
                    similarity = token.similarity(information_token)

                    if similarity > best_similarity:
                        best_similarity = similarity

                total_similarity += best_similarity

                if best_similarity >= 0:
                    count += 1

            if count > 0.1:
                results[information] = total_similarity / count

    for person in Person.objects.all():
        person_tags = [elem.text for elem in person.tags.all()]
        person_tokens = nlp(' '.join(person_tags))
        total_similarity = 0.0
        count = 0.0

        for token in tokens:
            best_similarity = -1
            for person_token in person_tokens:
                similarity = token.similarity(person_token)

                if similarity > best_similarity:
                    best_similarity = similarity

            total_similarity += best_similarity

            if best_similarity >= 0:
                count += 1

        if count > 0.1:
            results[person] = total_similarity / count

    sorted_results = sorted(results.items(), key=lambda kv: kv[1], reverse=True)
    if only_persons:
        res = 1
    else:
        res = 5
    return sorted_results[:res]


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
    get_matching_information(tags)


def identify_by_speech(recording):
    text = identify_speech.identify(recording)
    return json.loads(text)["processingResult"]["identifiedProfileId"]


def identify_by_image(image):
    identify_face.identify(image)


def identify_by_tag(tag):
    # TODO
    pass
