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

from  secondBrainBackend.models import Person,Information,Data

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def random_name(N):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))


def save_file(folder,name,file):
    fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
    # Generate random name
    filename = fs.save(name, file)
    file_path = fs.url(filename)
    return file_path

class AddPerson(TemplateView):
    template_name = 'add_person.html'

    # TODO post
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        phone = request.POST['phone']
        image = request.POST['image']
        address = request.POST['address']
        tags = request.POST['tags']
        if ',' in tags:
            tags = tags.split(',')
        else:
            tags = [tags]

        recording = request.POST['recording']
        random_name_prefix = random_name(10)

        image_name = '{}.jpg'.format(random_name_prefix)
        image_path = save_file(settings.images_storage_path,image)

        recording_name = '{}.wav'.format(random_name_prefix)
        image_path = save_file(settings.recordings_storage_path, recording)


        person = Person.objects.create(name=name,phone=phone,image_path=image_path,address=address)

        for tag in tags:
            person.tags.add(tag)

        person.save()


        # TODO save recording with random name
        # TODO save image in a certain location with random name
        # TODO recording saving
        # TODO here would be a call to generate a corresponding person in database

class AddInformation(TemplateView):
    template_name = 'add_information.html'

    # TODO post
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

        random_name_prefix = random_name(10)

        info = Information.objects.create()

        if image is not None:
            image_name = '{}.jpg'.format(random_name_prefix)
            image_name = save_file(settings.IMAGES_STORAGE_PATH, image_name,image)
            image_path = '{}/{}'.format(settings.IMAGES_STORAGE_PATH,image_name)

            image_data = Data.objects.create(data_type='image',path=image_path)

            info.data.add(image_data)

        if len(text) > 0 :
            note_data = Data.objects.create(data_type='text',text=text)

            info.data.add(note_data)


        for tag in tags:
            info.tags.add(tag)


        info.save(auto_tagging=True)


class IdentifyPerson(TemplateView):

    template_name = 'identify_person.html'

    # TODO post or get
    def post(self, request, *args, **kwargs):

        template = loader.get_template('results_person.html')
        context = {"name":"name1"
        }
        return HttpResponse(template.render(context, request))

class ResultsPerson(TemplateView):
    template_name = 'results_person.html'

    # TODO post or get
    def get(self, request, *args, **kwargs):
        template = loader.get_template('results_person.html')
        context = {}
        return HttpResponse(template.render(context, request))

class SearchTags(TemplateView):
    template_name =  'search_tags.html'
    def post(self, request, *args, **kwargs):

        #TODO first create embeddings, then search in our database

        template = loader.get_template('result_tags.html')
        list = [{"title":"title1", "text":"text1"}, {"title":"title2", "text":"text2"}, {"title":"title3", "text":"text3"}]
        context = {"list": list}
        return HttpResponse(template.render(context, request))

class ResultTags(TemplateView):
    template_name =  'result_tags.html'

    def get(self, request, *args, **kwargs):
        template = loader.get_template('result_tags.html')
        context = {}
        return HttpResponse(template.render(context, request))