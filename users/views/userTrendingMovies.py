from streaming_app_backend.mongo_client import movies_collection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def UserTrendingVideos(request):
    if request.method == "GET":
        # we have to fetch alll the trending videos by views maximum
        # we can add three columns for todays views,weekly views and all time views
        # later we can use any one of views for getting trending videos as per requirements
        # we can also use user choice preferences like if user is interested in some specific genre and language based trending
        trending_movies = (
            movies_collection.find({}, {"_id": 1, "name": 1, "fileLocation": 1})
            .sort("views", -1)
            .limit(10)
        )
        trending_movies_list = []
        for movies in trending_movies:
            print(movies)
            movies["_id"] = str(movies["_id"])
            trending_movies_list.append(movies)
        return JsonResponse({"movies": trending_movies_list})
    return JsonResponse({"msg": "method not allowed"})
