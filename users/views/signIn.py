from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import users_collection, genre_collection,languages_collection
from bson import ObjectId


@csrf_exempt
def signIn(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        email = body.get("email")
        password = body.get("password")
        # confirmPassword = body.get("confirmPassword")

        if not email:
            return JsonResponse({"msg": "email is not present"}, status=400)
        if not password:
            return JsonResponse({"msg": "password is not present"}, status=400)

        userResponse = users_collection.find_one({"email": email, "password": password})
        # userResponse["_id"]=str(userResponse["_id"])
        print(userResponse)
        if not userResponse:
            return JsonResponse(
                {
                    "msg": "No user Found with this email and password combination",
                    "success": False,
                },
                status=400,
            )
        else:
            updateLoggedInStatus = users_collection.update_one(
                {"_id": userResponse["_id"]}, {"$set": {"loggedInBefore": True}}
            )
            print(updateLoggedInStatus)
            if updateLoggedInStatus:
                userResponse["_id"] = str(userResponse["_id"])
                genreList = []
                for genreId in userResponse["selectedGenre"]:
                    genreData = genre_collection.find_one(
                        {"_id": ObjectId(genreId)}, {"_id": 1, "name": 1, "icon": 1}
                    )
                    genreData["_id"] = str(genreData["_id"])
                    genreList.append(genreData)
                userResponse["selectedGenre"] = genreList
                languageList = []
                for languageId in userResponse["selectedLanguages"]:
                    languageData = languages_collection.find_one(
                        {"_id": ObjectId(languageId)}, {"_id": 1, "name": 1}
                    )
                    languageData["_id"] = str(languageData["_id"])
                    languageList.append(languageData)
                userResponse["selectedLanguages"] = languageList
                return JsonResponse(
                    {"msg": "successfully logged in  ", "userData": userResponse},
                    status=200,
                )
    else:
        return JsonResponse({"msg": "wrong method"})
