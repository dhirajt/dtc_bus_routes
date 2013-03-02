from django.http import HttpResponse


def route(request):
    return HttpResponse("Hi, it worked!")

