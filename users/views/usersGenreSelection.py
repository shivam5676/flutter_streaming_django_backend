from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import users_collection


@csrf_exempt
def genreSelection(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        selectedGenre = body.get("genres")

        if len(selectedGenre) == 0:
            return JsonResponse(
                {"msg": "no genre is selected,please select a genre"}, status=400
            )
        for objectId in selectedGenre:
            # find the current object id in genre layout then (found genre) append it in array 
            genreResponse=""
        
        return JsonResponse(
            {"msg": "successfully logged in  ", "userData": "userResponse"},
            status=200,
        )
       

    else:
        return JsonResponse({"msg": "wrong method"})
