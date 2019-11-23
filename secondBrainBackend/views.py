from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))



class AddPerson(TemplateView):
    template_name = 'add_person.html'

    # TODO post
    def post(self, request, *args, **kwargs):
        name = request.POST['your_name']
        # TODO save image in a certain location with random name
        # TODO recording saving
        # TODO here would be a call to generate a corresponding person in database

class AddInformation(TemplateView):
    template_name = 'add_information.html'

    # TODO post
    def post(self, request, *args, **kwargs):
        print(request.POST)


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
        print(request.GET)

class SearchTags(TemplateView):
    template_name =  'search_tags.html'
    def post(self, request, *args, **kwargs):
        print(request.POST)

    # TODO post or get

class ResultTags(TemplateView):
    template_name =  'result_tags.html'

    def get(self, request, *args, **kwargs):
        print(request.GET)

    # TODO post or get
