from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Data
import json



# Create your views here.
def data_view(request):
    data = list(Data.objects.values("name"))
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        Data.objects.create(name=name)
        return HttpResponse(status=201)
    return HttpResponse(status=400)
