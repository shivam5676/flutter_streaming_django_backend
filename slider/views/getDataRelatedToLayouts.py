from streaming_app_backend.mongo_client import layouts_collection
from django.http import JsonResponse


def getDataRelatedToLayOuts():
    # we will get layout id and then we will fetch all the related movies and thier shorts there
    # we also can set limit for that we need to get starting and ending ids means we can decide how much data we have to send per request(optional)
    return JsonResponse({"msg": "method not allowed"})
