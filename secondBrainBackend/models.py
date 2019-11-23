from django.db import models

from abc import abstractmethod

from apis.image_tagging.image_tagging import get_tags_for_image
from apis.text_api.sendText import get_tags_for_text
from apis.face_api import detect as face_detect
from apis.speaker_recognition import create_enrollment, create_profile

import numpy as np


# class LocationData(Data):
#         pass

class Tag(models.Model):
    text = models.CharField(max_length=256)


class Person(models.Model):
    speech_id = models.CharField(max_length=256)
    image_id = models.CharField(max_length=256)
    image_path = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, related_name='person')
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    recording_path = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        tagging_needed = False
        if not self.pk:
            tagging_needed = True
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk

        super(Person, self).save(*args, **kwargs)

        # Handle azure cases
        self.image_id = face_detect.get_person_id(self.image_path)
        self.image_id = create_profile.create_person()
        create_enrollment.add_enrollment(self.recording_path)

    def __str__(self):
        string = "person_id: {}\n \
                 speech_id: {} \n \
                 image_id: {} \n \
                 tags: {} \n \
                 name: {}\n ".format(self.person_id, self.speech_id, self.image_id, self.tags, self.name)
        return string


class Data(models.Model):

    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()


class ImageData(Data):
    path = models.CharField(max_length=256)

    def get_tags(self):
        return get_tags_for_image(self.path)

    def __str__(self):
        return self.path


class NoteData(Data):
    text = models.CharField(max_length=256)

    def get_tags(self):
        return get_tags_for_text(self.text)

    def __str__(self):
        return self.text


class Information(models.Model):
    tags = models.ManyToManyField(Tag, related_name='information')
    data = models.OneToOneField(Data, on_delete=models.CASCADE)

    def get_additional_tags(self):
        additional_tags = self.data.get_tags()

        # TODO test this
        # TODO make sure no dublicates are getting created
        for additional_tag in additional_tags:
            new_tag = Tag.objects.get_or_create(additional_tag)
            self.tags.add(new_tag)

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

    def save(self, *args, **kwargs):
        tagging_needed = False
        if not self.pk:
            tagging_needed = True
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk

        super(Information, self).save(*args, **kwargs)
        self.get_additional_tags()

    def __str__(self):
        return str(self.data) + str(self.tags)

    def __repr__(self):
        return self.__str__()