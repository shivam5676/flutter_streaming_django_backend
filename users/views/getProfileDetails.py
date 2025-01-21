from django.http import JsonResponse
from streaming_app_backend.mongo_client import users_collection
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getProfileDetails(request):
    if request.method == "POST":
        body = json.loads(request.body)
        userId = request.userId
        userDetails = users_collection.find_one(
            {"_id": ObjectId(userId)},
            {"password": 0, "selectedGenre": 0, "selectedLanguages": 0},
        )
        
        userDetails['_id']=str(userDetails['_id'])
        return JsonResponse({"userDetails": userDetails})
    else:
        return JsonResponse({"msg": "method not allowed"})
