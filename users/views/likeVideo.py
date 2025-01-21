from django.http import JsonResponse
import json
from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def likeVideo(request):
    if request.method == "POST":
        body = json.loads(request.body)
        userId = request.userId
        shortsId = body.get("shortsId")
        user = users_collection.update_one(
            {"_id": ObjectId(userId)}, {"$push": {"LikedVideos": shortsId}}
        )

        

        try:
            return JsonResponse({"msg": "video liked"}, status=200)
        except:
            return JsonResponse({"msg": "video not Liked"})
    else:
        return JsonResponse({"msg": "method not allowed"}, status=400)
