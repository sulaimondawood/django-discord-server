from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello  world")    


def room(request):
    return HttpResponse("Hello Room")