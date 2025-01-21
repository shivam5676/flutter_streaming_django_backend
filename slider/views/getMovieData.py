from django.http import JsonResponse
from streaming_app_backend.mongo_client import movies_collection
from django.views.decorators.csrf import csrf_exempt
from streaming_app_backend.mongo_client import movies_collection, shorts_collection
import json
from bson import ObjectId
from users.views.checkSignedVideo import checkSignedVideo


@csrf_exempt
def getMovieData(request):
    if request.method == "POST":
       
        try:
            bodyData = json.loads(request.body)
        except Exception as err:
            print(err, "err")
        movieID = bodyData.get("movieID")

        data = movies_collection.find_one({"_id": ObjectId(movieID)})

        shorts = []

        if data:
            # Increment the 'views' field by 1
            movies_collection.update_one(
                {"_id": ObjectId(movieID)}, {"$inc": {"views": 1}}
            )

            
            trailerUrl = data.get("trailerUrl")
            low = data.get("low")
            medium = data.get("medium")
            high = data.get("high")
            shorts.append(
                {
                    "trailerUrl": checkSignedVideo(trailerUrl),
                    "low": checkSignedVideo(low),
                    "medium": checkSignedVideo(medium),
                    "high": checkSignedVideo(high),
                }
            )  # later we will change this to fileLocation because now i am taking direct video serving link and for shorts we are using localhost:8765 so later we will replace localhost with direct link
            # print(trailerUrl)
            if data.get("shorts"):
                for currentShortsID in data["shorts"]:
                    if currentShortsID == "Ads":
                        shorts.append({"type": "Promotional Ads"})
                    else:
                        if isinstance(currentShortsID, str):
                            currentShortsID = ObjectId(currentShortsID)

                        shortsData = shorts_collection.find_one(
                            {
                                "_id": currentShortsID,
                            },
                            {"genre": 0, "language": 0},
                        )

                        if shortsData:
                            # Convert ObjectId fields to strings in shortsData
                            shortsData["_id"] = str(shortsData["_id"])
                            shortsData["low"] = checkSignedVideo(shortsData.get("low"))
                            shortsData["medium"] = checkSignedVideo(
                                shortsData.get("medium")
                            )
                            shortsData["high"] = checkSignedVideo(shortsData.get("high"))
                            
                            # Add more fields to convert if needed

                            shorts.append(shortsData)
        return JsonResponse({"shortsData": shorts},status=200)

    # moviesData = movies_collection.find_one({_id: request.params.id})
    return JsonResponse({"msg": "method not allowed"},status=500)
