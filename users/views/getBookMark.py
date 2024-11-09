from django.http import JsonResponse
import json
from streaming_app_backend.mongo_client import users_collection, shorts_collection
from bson import ObjectId

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getBookMark(request):
    if request.method == "POST":
        body = json.loads(request.body)
        userId = body.get("userId")
        # shortsId = body.get("shortsId")
        user = users_collection.find_one(
            {"_id": ObjectId(userId)},
        )
        if not user:
            return JsonResponse({"msg": "no user found"}, status=400)
        try:
            print(user)
            if user and user["BookMark"]:

                bookMarkData = []
                for shortsId in user["BookMark"]:
                    print(shortsId, "sid")
                    print(shortsId)
                    if shortsId:
                        shortsData = shorts_collection.find_one(
                            {
                                "_id": ObjectId(shortsId),
                            },
                            {"genre": 0, "language": 0},
                        )

                        if shortsData:
                            shortsData["_id"] = str(shortsData["_id"])
                            bookMarkData.append(shortsData)
                    else:
                        print("invalid short id")
                return JsonResponse(
                    {"msg": "bookmarked data is here", "bookMarkData": bookMarkData},
                    status=200,
                )
            else:
                return JsonResponse(
                    {"msg": "bookmarked data not found", "bookMarkData": []}, status=200
                )

        except:
            return JsonResponse({"msg": "something went wrong"}, status=500)
    else:
        return JsonResponse({"msg": "method not allowed"}, status=400)
