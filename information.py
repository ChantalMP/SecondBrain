from abc import abstractmethod
from typing import List, Optional

from apis.text_api.sendText import get_tags_for_text
from apis.image_tagging.image_tagging import get_tags_for_image

import numpy as np
import pickle

class Data:
    def __init__(self):
        pass

    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

class ImageData(Data):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def get_tags(self):
        return get_tags_for_image(self.path)

    def __str__(self):
        return self.path


class NoteData(Data):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def get_tags(self):
        return get_tags_for_text(self.text)

    def __str__(self):
        return self.text


# class LocationData(Data):
#         pass


class Information:

    def __init__(self, data: Data, tags: Optional[List[str]]):
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        self.data = data

        additional_tags = self.data.get_tags()

        self.tags += additional_tags  # TODO create word embedding for these

    def compare_tags(self, obj_tags):
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

    def __str__(self):
        return str(self.data) + str(self.tags)

    def __repr__(self):
        return self.__str__()



def create_information(data: Data, tags=None):
    '''
    :param data: image,note,location
    '''

    information = Information(data, tags)
    return information


def find_matching_infos(tags, informations):
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
        tags = get_tags_for_image(raw_data)
    else:
        if ',' in raw_data:
            tags = raw_data.split(',')
        else:
            tags = [raw_data]

    # here we should have tags
    find_matching_infos(tags, informations)

import os
if __name__ == '__main__':

    from database import informations

    note_data = NoteData('How does my dog look like? And how does my cat look like')
    informations.append(create_information(note_data))

    image_data = ImageData('apis/face_api/images/IMG_2629.jpg')
    informations.append(create_information(image_data))


    pickle.dump(informations,open( "database/informations.p", "wb" ))

    tags = 'dog'
    process_input(tags, informations)
