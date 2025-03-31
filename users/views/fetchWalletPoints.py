from django.http import JsonResponse
from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fetchWalletPoints(request):
    if request.method == "GET":
        userId = request.userId
        userData = users_collection.find_one(
            {"_id": ObjectId(userId)}, {"allocatedPoints": 1, "_id": 1}
        )
        
        if not userData:
         return JsonResponse({"msg": "err while fetching the user. please provide a valid token"}, status=400)
        return JsonResponse({"allocatedPoints": userData.get("allocatedPoints")}, status=200)
    else:
        
        return JsonResponse({"msg": "Method not allowed"}, status=200)
