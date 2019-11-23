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
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')

class AddInformation(TemplateView):
    template_name = 'add_information.html'

    # TODO post


class IdentifyPerson(TemplateView):
    template_name = 'identify_person.html'

    # TODO post or get

class SearchInformation(TemplateView):
    template_name =  'search_information.html'

    # TODO post or get