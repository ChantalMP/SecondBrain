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

import apis.face_api.identify as faceAPI
import apis.speaker_recognition.identify as speechAPI

from apis.image_tagging.image_tagging import get_tags_for_image
from apis.text_api.sendText import get_tags_for_text

from secondBrainBackend.utils import get_matching_information


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
        phone = request.POST['your_phone']
        address = request.POST['your_adress']
        try:
            image = request.FILES['image']

        except Exception as e:
            image = None

        try:
            recording = request.FILES['audio']

        except Exception as e:
            recording = None

        tags = request.POST['tags']

        if ',' in tags:
            tags = tags.split(',')
        elif len(tags) > 0:
            tags = [tags]
        else:
            tags = []

        random_name_prefix = random_name()

        person = Person.objects.create(name=name, phone=phone, address=address)

        for tag in tags:
            new_tag, _ = Tag.objects.get_or_create(text=tag)
            person.tags.add(new_tag)

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

        info = Information.objects.create(title=title)

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
        random_name_prefix = random_name(10)
        try:
            image = request.FILES['image']

        except Exception as e:
            image = None
        info = Information.objects.create()

        try:
            recording = request.FILES['audio']

        except Exception as e:
            recording = None

        if image is not None:
            image_name = '{}.jpg'.format(random_name_prefix)
            image_name = save_file(settings.IMAGES_STORAGE_PATH, image_name, image)
            image_path = '{}/{}'.format(settings.IMAGES_STORAGE_PATH, image_name)

            image_data = Data.objects.create(data_type='image', path=image_path)

            info.data.add(image_data)

            image_id = faceAPI.identify(image_path)
            person_name = Person.objects.get(image_id=image_id).name
            image_path = Person.objects.get(image_id=image_id).image_path.split('/')

        elif recording is not None:
            recording_name = '{}.wav'.format(random_name_prefix)
            recording_name = save_file(settings.RECORDING_STORAGE_PATH, recording_name, recording)
            recording_path = '{}/{}'.format(settings.RECORDING_STORAGE_PATH, recording_name)

            audio_id = speechAPI.identify(recording_path)
            person_name = Person.objects.get(audio_id=audio_id).name
            image_path = Person.objects.get(audio_id=audio_id).image_path.split('/')
        image_path = image_path[2] + '/' + image_path[3]
        template = loader.get_template('results_person.html')
        context = {"name": person_name,
                   "image_path": image_path
                   }
        print(image_path)
        return HttpResponse(template.render(context, request))


class ResultsPerson(TemplateView):
    template_name = 'results_person.html'

    def get(self, request, *args, **kwargs):
        template = loader.get_template('results_person.html')
        context = {}
        return HttpResponse(template.render(context, request))


class SearchTags(TemplateView):
    template_name = 'search_tags.html'

    def post(self, request, *args, **kwargs):

        all_tags = []

        tags = (request.POST['tags'])
        if ',' in tags:
            tags = tags.split(',')
            all_tags += tags
        elif len(tags) > 0:
            all_tags.append(tags)

        query = request.POST['query']
        if len(query) > 0:
            all_tags += get_tags_for_text(query)

        try:
            image = request.FILES['image']
            random_name_prefix = random_name()
            image_name = '{}.jpg'.format(random_name_prefix)
            image_name = save_file(settings.IMAGES_STORAGE_PATH, image_name, image)
            image_path = '{}/{}'.format(settings.IMAGES_STORAGE_PATH, image_name)
            all_tags += get_tags_for_image(image_path)
        except Exception as e:
            image = None

        result_list = get_matching_information(all_tags)

        results_list_filtered = [elem[0] for elem in result_list]

        parsed_informations = []
        parsed_persons = []

        for elem in results_list_filtered:
            if isinstance(elem, Information):
                information = elem
                information_dict = {}
                information_dict['title'] = information.title
                datas = []

                for data in information.data.all():
                    data_dict = {}
                    if data.path is not None:
                        image_path = data.path.split('/')
                        image_path = image_path[2] + '/' + image_path[3]
                        data_dict['image_path'] = image_path
                    else:
                        data_dict['image_path'] = None
                    data_dict['text'] = data.text

                    datas.append(data_dict)

                information_dict['datas'] = datas

                parsed_informations.append(information_dict)

            else:
                person = elem
                person_dict = {}
                person_dict['name'] = person.name

                if person.image_path is not None:
                    image_path = person.image_path.split('/')
                    image_path = image_path[2] + '/' + image_path[3]
                    person_dict['image_path'] = image_path
                else:
                    person_dict['image_path'] = None

                person_dict['address'] = person.address
                person_dict['phone'] = person.phone

                parsed_persons.append(person_dict)

        template = loader.get_template('result_tags.html')
        context = {"results_informations": parsed_informations, "results_persons": parsed_persons}
        return HttpResponse(template.render(context, request))


class ResultTags(TemplateView):
    template_name = 'result_tags.html'

    def get(self, request, *args, **kwargs):
        template = loader.get_template('result_tags.html')
        context = {}
        return HttpResponse(template.render(context, request))
