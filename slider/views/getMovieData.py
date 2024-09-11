from django.http import JsonResponse
from streaming_app_backend.mongo_client import movies_collection
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def getMovieData(request):
    if request.method == "POST":
        print(request)
    print(request)
    # moviesData = movies_collection.find_one({_id: request.params.id})
    return JsonResponse({})
