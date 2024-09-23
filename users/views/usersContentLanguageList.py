from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import languages_collection


@csrf_exempt
def usersContentLanguageList(request):
    if request.method == "GET":
        languageArray = []
        languageList = languages_collection.find()
        print(languageList)
        for language in languageList:
            language['_id']=str(language['_id'])
            languageArray.append(language)
        return JsonResponse({"languageList": languageArray})
    else:
        return JsonResponse({"msg": "method not allowed"})
