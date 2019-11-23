from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

import random
import string

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from django.core.files.storage import FileSystemStorage

from django.conf import settings

from secondBrainBackend.models import Person, Information, Data, Tag


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def random_name(N=20):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def save_file(folder, name, file):
    fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
    # Generate random name
    filename = fs.save(name, file)
    file_path = fs.url(filename)
    return file_path


class AddPerson(TemplateView):
    template_name = 'add_person.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['your_name']
        phone = request.POST['phone']
        address = request.POST['your_adress']
        try:
            image = request.FILES['image']

        except Exception as e:
            image = None

        try:
            recording = request.FILES['recording']

        except Exception as e:
            recording = None

        tags = request.POST['tags']

        if ',' in tags:
            tags = tags.split(',')
        elif len(tags) > 0:
            tags = [tags]
        else:
            tags = []

        recording = request.POST['recording']
        random_name_prefix = random_name()

        image_name = '{}.jpg'.format(random_name_prefix)


        person = Person.objects.create(name=name, phone=phone,address=address)

        for tag in tags:
            person.tags.add(tag)

        person.save()


        if image is not None:
            image_name = '{}.jpg'.format(random_name_prefix)
            image_name = save_file(settings.IMAGES_STORAGE_PATH, image_name, image)
            image_path = '{}/{}'.format(settings.IMAGES_STORAGE_PATH, image_name)

            person.image_path = image_path

            person.save()

        if recording is not None:
            recording_name = '{}.wav'.format(random_name_prefix)
            recording_name = save_file(settings.RECORDING_STORAGE_PATH, recording_name, recording)
            recording_path = '{}/{}'.format(settings.RECORDING_STORAGE_PATH, recording_name)

            person.recording_path = recording_path

            person.save()

        for tag in tags:
            new_tag, _ = Tag.objects.get_or_create(text=tag)

            person.tags.add(new_tag)

        person.save(auto_tagging=True)

        return HttpResponse("Success!")


class AddInformation(TemplateView):
    template_name = 'add_information.html'

    def post(self, request, *args, **kwargs):
        tags = request.POST['tags']
        title = request.POST['info_title']
        try:
            image = request.FILES['image']

        except Exception as e:
            image = None
        text = request.POST['note']
        tags = request.POST['tags']

        if ',' in tags:
            tags = tags.split(',')
        elif len(tags) > 0:
            tags = [tags]
        else:
            tags = []

        random_name_prefix = random_name()

        info = Information.objects.create()

        if image is not None:
            image_name = '{}.jpg'.format(random_name_prefix)
            image_name = save_file(settings.IMAGES_STORAGE_PATH, image_name, image)
            image_path = '{}/{}'.format(settings.IMAGES_STORAGE_PATH, image_name)

            image_data = Data.objects.create(data_type='image', path=image_path)

            info.data.add(image_data)

        if len(text) > 0:
            note_data = Data.objects.create(data_type='text', text=text)

            info.data.add(note_data)

        for tag in tags:
            new_tag, _ = Tag.objects.get_or_create(text=tag)
            info.tags.add(new_tag)

        info.save(auto_tagging=True)

        return HttpResponse("Success!")


class IdentifyPerson(TemplateView):
    template_name = 'identify_person.html'

    # TODO post or get
    def post(self, request, *args, **kwargs):
        template = loader.get_template('results_person.html')
        context = {"name": "name1"
                   }
        return HttpResponse(template.render(context, request))


class ResultsPerson(TemplateView):
    template_name = 'results_person.html'

    # TODO post or get
    def get(self, request, *args, **kwargs):
        print(request.GET)


class SearchTags(TemplateView):
    template_name = 'search_tags.html'

    def post(self, request, *args, **kwargs):

        #TODO first create embeddings, then search in our database

        template = loader.get_template('result_tags.html')
        list = [{"title":"title1", "text":"text1"}, {"title":"title2", "text":"text2"}, {"title":"title3", "text":"text3"}]
        context = {"list": list}
        return HttpResponse(template.render(context, request))


class ResultTags(TemplateView):
    template_name = 'result_tags.html'

    def get(self, request, *args, **kwargs):
        print(request.GET)