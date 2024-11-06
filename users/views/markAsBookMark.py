from django.http import JsonResponse
import json
from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId


def markAsBookMark(request):
    body = json.loads(request.body)
    userId = body.get("userId")
    shortsId = body.get("shortsId")
    user = users_collection.update_one(
        {"_id": ObjectId(userId)}, {"$push": {"BookMark": shortsId}}
    )

    print(user)

    try:
        return JsonResponse({"msg": "video bookmarked"},status=200)
    except:
        return JsonResponse({"msg": "video not bookmarked"})
