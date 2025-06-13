from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
    return JsonResponse({"message": "Hello, From the room booking app!"})