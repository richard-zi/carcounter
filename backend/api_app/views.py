from django.shortcuts import render
from django.http import JsonResponse
from .models import Data
# Create your views here.


def data_view(request):
    data = list(Data.objects.values("name"))
    return JsonResponse(data, safe=False)
