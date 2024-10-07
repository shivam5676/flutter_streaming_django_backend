from django.http import JsonResponse
from streaming_app_backend.mongo_client import movies_collection, shorts_collection


def TrailerTrendingSection(request):
    if request.method == "GET":
        moviesData = movies_collection.find(
            {}, {"_id": 1, "name": 1, "shorts": 1, "trailerUrl": 1}
        ).limit(10)
        moviesArray = []
        for movie in moviesData:
            print(movie)
            movie["_id"] = str(movie["_id"])
            shortsArray = []
            for shortid in movie["shorts"]:
                shortsData = shorts_collection.find_one(
                    {"_id": shortid, "visible": True},
                    {"_id": 1, "name": 1, "fileLocation": 1},
                )
                shortsData["_id"] = str(shortsData["_id"])
                shortsArray.append(shortsData)
                print(shortsData)
            movie["shorts"] = shortsArray
            moviesArray.append(movie)
        return JsonResponse({"trailersData": moviesArray})
    else:
        return JsonResponse({"msg": "method not allowed"})
