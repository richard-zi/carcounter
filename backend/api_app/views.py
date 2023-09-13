from django.http import JsonResponse
from .models import VehicleData
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime


@csrf_exempt
def save_vehicle_data(request):
    if request.method == "POST":
        data = request.POST
        vehicle = data.get('vehicle')
        direction = data.get('direction')
        naive_datetime = datetime.strptime(data.get('timestamp'), '%Y-%m-%d %H:%M:%S')
        aware_datetime = timezone.make_aware(naive_datetime)
        
        # Daten in der Datenbank speichern
        VehicleData.objects.create(vehicle=vehicle, direction=direction, timestamp=aware_datetime)
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)

    
def get_all_vehicle_data(request):
    if request.method == "GET":
        data_list = []
        for obj in VehicleData.objects.all():
            data_list.append({
                "vehicle": obj.vehicle,
                "direction": obj.direction,
                "timestamp": obj.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return JsonResponse({"data": data_list}, status=200)
    else:
        return JsonResponse({"status": "invalid request"}, status=400)

