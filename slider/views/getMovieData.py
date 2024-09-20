from django.http import JsonResponse
from streaming_app_backend.mongo_client import movies_collection
from django.views.decorators.csrf import csrf_exempt
from streaming_app_backend.mongo_client import movies_collection, shorts_collection
import json
from bson import ObjectId


@csrf_exempt
def getMovieData(request):
    if request.method == "POST":
        bodyData = json.loads(request.body)
        movieID = bodyData.get("movieID")

        data = movies_collection.find_one({"_id": ObjectId(movieID)})
        
        shorts = []
        if data and data["shorts"]:
            for currentShortsID in data["shorts"]:
                shortsData = shorts_collection.find_one({"_id": currentShortsID})
                if shortsData:
                    # Convert ObjectId fields to strings in shortsData
                    shortsData["_id"] = str(shortsData["_id"])

                    # Add more fields to convert if needed

                    shorts.append(shortsData)
        return JsonResponse({"shortsData": shorts})

    # moviesData = movies_collection.find_one({_id: request.params.id})
    return JsonResponse({"msg": "method not allowed"})
