from django.http import JsonResponse
from streaming_app_backend.mongo_client import checkInPoints
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
@csrf_exempt
def dailyCheckInTask(request):
    if request.method == "POST":
        body = json.loads(request.body)
        userId = body.get("userId")
        print(userId)
        response = checkInPoints.find({"assignedUser": userId})
        for data in response:
            print(data)
        return JsonResponse({"msg": "checkIn Called"})
