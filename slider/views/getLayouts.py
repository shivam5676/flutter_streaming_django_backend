from streaming_app_backend.mongo_client import layouts_collection, movies_collection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def getLayouts(request):
    if request.method == "GET":
        layoutsResult = layouts_collection.find({}, {"_id": 1, "linkedMovies": 1,"name":1})
        layOutsData = {}
        for layout in layoutsResult:
            # print(layout["linkedMovies"], "LM")
            currentLayoutObj = []
            # Limit the linked movies to the first 6
            linkedMovies = layout["linkedMovies"][:6]
            currentLayoutObj.append({"layoutId":str(layout["_id"]),"layoutName":layout["name"]})
            for currentMovie in linkedMovies:
                # print(currentMovie, "currentMovie")
                movieData = movies_collection.find_one(
                    {"_id": currentMovie}, {"fileLocation": 1, "name": 1}
                )
                # print(movieData)
                movieData["_id"] = str(movieData["_id"])
                
                currentLayoutObj.append(movieData)
            layOutsData[str(layout["_id"])] = currentLayoutObj
        print(layOutsData)
        return JsonResponse({"layouts": layOutsData})

    return JsonResponse({"msg": "method not allowed"})