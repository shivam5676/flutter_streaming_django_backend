from streaming_app_backend.mongo_client import layouts_collection, movies_collection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId


@csrf_exempt
def getDataRelatedToLayOuts(request,movieID):
    
    print(movieID)
    # we will get layout id and then we will fetch all the related movies and thier shorts there
    # we also can set limit for that we need to get starting and ending ids means we can decide how much data we have to send per request(optional)
    if request.method == "GET":
        result = layouts_collection.find({"_id": ObjectId(movieID)})
        movieObj = []
        for layout in result:
            linkedMovies = layout["linkedMovies"]
            for currentMovieId in linkedMovies:
                #   print(currentMovieId)
                movieData = movies_collection.find_one(
                    {"_id": currentMovieId}, {"fileLocation": 1, "name": 1}
                )
                movieData['_id']=str(movieData['_id'])
                movieObj.append(movieData)
               
        return JsonResponse({"moviesList": movieObj})
    return JsonResponse({"msg": "method not allowed"})
