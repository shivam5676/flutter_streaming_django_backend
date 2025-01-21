from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId


@csrf_exempt
def genreSelection(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        selectedGenre = body.get("selectedGenre")
        userId = request.userId
        if len(selectedGenre) == 0:
            return JsonResponse(
                {"msg": "no genre is selected,please select a genre"}, status=400
            )

        updatedData = users_collection.update_one(
            {"_id": ObjectId(userId)}, {"$set": {"selectedGenre": selectedGenre}}
        )
        if updatedData:
            # validUser["selectedGenre"] = selectedGenre
            return JsonResponse(
                {
                    "msg": "successfully selected the genre  ",
                    "userData": "userResponse",
                },
                status=200,
            )
        else:
            return JsonResponse({"msg": "user is invalid"})
    else:
        return JsonResponse({"msg": "wrong method"})
