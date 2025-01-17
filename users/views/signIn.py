from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timezone
from streaming_app_backend.mongo_client import (
    users_collection,
    genre_collection,
    languages_collection,
)
from bson import ObjectId
from helper_function.tokenCreator import tokenCreator
from helper_function.updateLoginStatus import updateLoginStatus


@csrf_exempt
def signIn(request):
    # tokenCreator({"name":"shivam","class":"9th"})
    # print(request.userId)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        email = body.get("email")
        password = body.get("password")
        fcmtoken = body.get("nId")  # notification id
        deviceType = body.get("deviceType")

        if not email:
            return JsonResponse({"msg": "email is not present"}, status=400)
        if not password:
            return JsonResponse({"msg": "password is not present"}, status=400)
        # if not fcmtoken:
        #     return JsonResponse(
        #         {"msg": "please give us access for notification"}, status=400
        #     )

        userResponse = users_collection.find_one(
            {"email": email, "password": password}, {"password": 0}
        )

        if not userResponse:
            return JsonResponse(
                {
                    "msg": "No user Found with this email and password combination",
                    "success": False,
                },
                status=400,
            )
        else:
            try:

                updatedUserResponse, token = updateLoginStatus(
                    userResponse, fcmtoken, deviceType
                )
                return JsonResponse(
                    {
                        "msg": "successfully logged in",
                        "userData": updatedUserResponse,
                        "token": token,
                    },
                    status=200,
                )
            except Exception as err:
                return JsonResponse({"msg": str(err)})
            # updateLoggedInStatus = users_collection.update_one(
            #     {"_id": userResponse["_id"]}, {"$set": {"loggedInBefore": True}}
            # )

            # if updateLoggedInStatus:
            #     token = tokenCreator({"id": str(userResponse["_id"])})

            #     genreList = []
            #     if "selectedGenre" in userResponse and userResponse["selectedGenre"]:
            #         for genreId in userResponse["selectedGenre"]:
            #             genreData = genre_collection.find_one(
            #                 {"_id": ObjectId(genreId)}, {"_id": 1, "name": 1, "icon": 1}
            #             )
            #             genreData["_id"] = str(genreData["_id"])
            #             genreList.append(genreData)
            #     userResponse["selectedGenre"] = genreList
            #     languageList = []
            #     if (
            #         "selectedLanguages" in userResponse
            #         and userResponse["selectedLanguages"]
            #     ):
            #         for languageId in userResponse["selectedLanguages"]:
            #             languageData = languages_collection.find_one(
            #                 {"_id": ObjectId(languageId)}, {"_id": 1, "name": 1}
            #             )
            #             languageData["_id"] = str(languageData["_id"])
            #             languageList.append(languageData)
            #     userResponse["selectedLanguages"] = languageList
            #     if not userResponse.get("Devices"):
            #         updatedResponse = users_collection.update_one(
            #             {"_id": ObjectId(userResponse["_id"])},
            #             {
            #                 "$set": {
            #                     "Devices": [
            #                         {
            #                             "fcmtoken": fcmtoken,
            #                             "deviceType": deviceType or "web",
            #                             "lastUpdated": datetime.now(timezone.utc),
            #                         }
            #                     ]
            #                 }
            #             },
            #         )
            #     else:
            #         userDevices = userResponse.get("Devices")
            #         idIsPresent = False
            #         print("hello", userDevices)
            #         for device in userDevices:
            #             if device["fcmtoken"] == fcmtoken:
            #                 idIsPresent = True

            #                 break

            #         if not idIsPresent:
            #             userDevices.append(
            #                 {
            #                     "fcmtoken": fcmtoken,
            #                     "deviceType": deviceType,
            #                     "lastUpdated": datetime.now(timezone.utc),
            #                 }
            #             )
            #             updatedResponse = users_collection.update_one(
            #                 {"_id": ObjectId(userResponse["_id"])},
            #                 {"$set": {"Devices": userDevices}},
            #             )
            #             print(updatedResponse, "up>>>>>")
            #     userResponse["Devices"] = [
            #         {
            #             "fcmtoken": fcmtoken,
            #             "deviceType": deviceType,
            #             "lastUpdated": datetime.now(timezone.utc),
            #         }
            #     ]

            #     userResponse["_id"] = ""
            # return JsonResponse(
            #     {
            #         "msg": "successfully logged in",
            #         "userData": userResponse,
            #         "token": token,
            #     },
            #     status=200,
            # )
    else:
        return JsonResponse({"msg": "wrong method"})
