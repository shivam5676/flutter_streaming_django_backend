from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import genre_collection


@csrf_exempt
def genreList(request):
    if request.method == "GET":
        genresArray = []
        genrelist = genre_collection.find({},{"_id":1,"name":1,"icon":1})
        
        for genre in genrelist:
            genre['_id']=str(genre['_id'])
            genresArray.append(genre)
        return JsonResponse({"genreList": genresArray})
    else:
        return JsonResponse({"msg": "method not allowed"})
