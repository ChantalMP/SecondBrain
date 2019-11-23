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
    # TODO name should be tag
    speech_id = models.CharField(max_length=256,null=True,blank=True)
    image_id = models.CharField(max_length=256,null=True,blank=True)
    image_path = models.CharField(max_length=256,null=True,blank=True)
    tags = models.ManyToManyField(Tag, related_name='person')
    name = models.CharField(max_length=256,null=True,blank=True)
    address = models.CharField(max_length=256,null=True,blank=True)
    phone = models.CharField(max_length=256,null=True,blank=True)
    recording_path = models.CharField(max_length=256,null=True,blank=True)

    # TODO test this save method
    def save(self, auto_tagging=False,*args, **kwargs):
        super(Person, self).save(*args, **kwargs)

        if auto_tagging:
            # Handle azure cases
            self.image_id = face_detect.get_person_id(self.image_path)
            self.speech_id = create_profile.create_person()
            create_enrollment.add_enrollment(self.recording_path)

            self.save()

    def __str__(self):
        string = "person_id: {}\n \
                 speech_id: {} \n \
                 image_id: {} \n \
                 tags: {} \n \
                 name: {}\n ".format(self.person_id, self.speech_id, self.image_id, self.tags, self.name)
        return string


class Information(models.Model):
    tags = models.ManyToManyField(Tag, related_name='information')
    # TODO This becomes foreign key, make sure it works correcly
    # TODO TITLE and is also a tag
    # TODO compare tags should also be tag

    def get_additional_tags(self):
        # TODO ITERATE OVER DATA
        for d in self.data.all():
            additional_tags = d.get_tags()

            # TODO test this
            # TODO make sure no dublicates are getting created
            for additional_tag in additional_tags:
                new_tag = Tag.objects.get_or_create(additional_tag)
                self.tags.add(new_tag)


    def save(self, auto_tagging=False,*args, **kwargs):

        super(Information, self).save(*args, **kwargs)
        if auto_tagging:
            self.get_additional_tags()
            self.save()

    def __str__(self):
        return str(self.data) + str(self.tags)

    def __repr__(self):
        return self.__str__()



class Data(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE,related_name='data',null=True)


    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def __str__(self):
        pass



class ImageData(Data):
    path = models.CharField(max_length=256)

    def get_tags(self):
        return get_tags_for_image(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path


class NoteData(Data):
    # TODO make area
    text = models.CharField(max_length=256)

    def get_tags(self):
        return get_tags_for_text(self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text