from django.http import JsonResponse
import json
from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt

def markAsBookMark(request):
 if request.method == "POST":
    body = json.loads(request.body)
    userId = request.userId
    shortsId = body.get("shortsId")
    user = users_collection.update_one(
        {"_id": ObjectId(userId)}, {"$push": {"BookMark": shortsId}}
    )

    

    try:
        return JsonResponse({"msg": "video bookmarked"},status=200)
    except:
        return JsonResponse({"msg": "video not bookmarked"},status=400)
 else:
     return JsonResponse({"msg": "method not allowed"},status=400)