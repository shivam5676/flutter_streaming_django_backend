from django.http import JsonResponse
from streaming_app_backend.mongo_client import users_collection
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def editProfileDetails(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            email = body.get("email")
            name = body.get("name")
            gender = body.get("gender")
            mobile = body.get("mobile")
            body = json.loads(request.body)
            userId = request.userId
            userDetails = users_collection.find_one_and_update(
                {"_id": ObjectId(userId)},
                {
                    "$set": {
                        "email": email,
                        "mobile": mobile,
                        "name": name,
                        "gender": gender,
                    }
                },
            )
            print(userDetails)
            userDetails["_id"] = str(userDetails["_id"])
            return JsonResponse({"userDetails": userDetails})
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"msg": "method not allowed"})
