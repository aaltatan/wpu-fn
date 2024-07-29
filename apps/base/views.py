from django.shortcuts import render
from django.http import HttpRequest, HttpResponse



def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'apps/base/index.html')


def get_messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'partials/messages.html')
