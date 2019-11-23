from django.db import models

from abc import abstractmethod

from apis.image_tagging.image_tagging import get_tags_for_image
from apis.text_api.sendText import get_tags_for_text
from apis.face_api import identify as face_identify
from apis.speaker_recognition import create_enrollment, create_profile

import numpy as np


# class LocationData(Data):
#         pass

class Tag(models.Model):
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text


class Person(models.Model):

    speech_id = models.CharField(max_length=256,null=True,blank=True)
    image_id = models.CharField(max_length=256,null=True,blank=True)
    image_path = models.CharField(max_length=256,null=True,blank=True)
    tags = models.ManyToManyField(Tag, related_name='person')
    name = models.CharField(max_length=256,null=True,blank=True)
    address = models.CharField(max_length=256,null=True,blank=True)
    phone = models.CharField(max_length=256,null=True,blank=True)
    recording_path = models.CharField(max_length=256,null=True,blank=True)

    def save(self, auto_tagging=False,*args, **kwargs):
        super(Person, self).save(*args, **kwargs)

        if auto_tagging:
            # Handle azure cases
            self.image_id = face_identify.create_peson(self.name)
            face_identify.add_image_to_person(self.image_id, self.image_path)
            self.speech_id = create_profile.create_person()
            create_enrollment.add_enrollment(self.recording_path,self.speech_id)

            self.save()

    def __str__(self):
        string = "person_id: {}\n \
                 speech_id: {} \n \
                 image_id: {} \n \
                 tags: {} \n \
                 name: {}\n ".format(self.person_id, self.speech_id, self.image_id, self.tags, self.name)
        return string

    def __repr__(self):
        string = "person_id: {}\n \
                         speech_id: {} \n \
                         image_id: {} \n \
                         tags: {} \n \
                         name: {}\n ".format(self.person_id, self.speech_id, self.image_id, self.tags, self.name)
        return string


class Information(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='information')

    def get_additional_tags(self):
        for d in self.data.all():
            additional_tags = d.get_tags()

            for additional_tag in additional_tags:
                new_tag,_ = Tag.objects.get_or_create(text=additional_tag)
                self.tags.add(new_tag)
        if self.title:
            for tag in self.title.split(' '):
                new_tag, _ = Tag.objects.get_or_create(text=tag)
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
    data_type = models.CharField(max_length=256) # image or text
    path = models.CharField(max_length=256,null=True,blank=True)
    text = models.CharField(max_length=256,null=True,blank=True)

    def get_tags(self):
        if self.data_type == 'image':
            return get_tags_for_image(self.path)
        else:
            return get_tags_for_text(self.text)

    def __str__(self):
        if self.data_type == 'image':
            return self.path
        else:
            return self.text
