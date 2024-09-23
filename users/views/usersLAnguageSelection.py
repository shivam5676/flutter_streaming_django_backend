from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import languages_collection, users_collection
from bson import ObjectId


@csrf_exempt
def usersLanguaseSelection(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        selectedLanguages = body.get("selectedLanguages")
        userId = body.get("userId")
        if len(selectedLanguages) == 0:
            return JsonResponse(
                {"msg": "no language is selected,please select a language first"},
                status=400,
            )

        updatedData = users_collection.update_one(
            {"_id": ObjectId(userId)},
            {"$set": {"selectedLanguages": selectedLanguages}},
        )
        if updatedData:
            # validUser["selectedGenre"] = selectedGenre
            return JsonResponse(
                {"msg": "successfully saved the languages  ", "success": True},
                status=200,
            )
        else:
            return JsonResponse({"msg": "user is invalid"})
    else:
        return JsonResponse({"msg": "wrong method"})
