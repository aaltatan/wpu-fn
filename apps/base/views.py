from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


part_template_: str = lambda x: f'apps/base/partials/{x}.html'


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'apps/base/index.html')


def get_messages(request: HttpRequest) -> HttpResponse:
    return render(request, part_template_('messages'))
