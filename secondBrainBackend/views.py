from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.http import HttpResponse
from django.template import loader

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))