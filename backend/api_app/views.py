from django.http import JsonResponse
from django.http import JsonResponse
from .models import VehicleData
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_vehicle_data(request):
    if request.method == "POST":
        data = request.POST
        vehicle = data.get('vehicle')
        direction = data.get('direction')
        timestamp = data.get('timestamp')
        
        # Daten in der Datenbank speichern
        VehicleData.objects.create(vehicle=vehicle, direction=direction, timestamp=timestamp)
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)