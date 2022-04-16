from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    try:
        echostr = request.GET["echostr"]
        return HttpResponse(echostr)
    except MultiValueDictKeyError:
        return HttpResponse("Hello, world. You're at the polls index.")
