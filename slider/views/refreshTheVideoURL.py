from users.views.checkSignedVideo import checkSignedVideo
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt

def refreshTheVideoURL(request):
   
    if request.method == "POST": 
        print("hello",request.body.decode('utf-8'))
        try:
            body = json.loads(request.body)
            print(body)        
            data = checkSignedVideo(body.get("url"))

            return JsonResponse({"data": data}, status=200)
        except Exception as e:
            return JsonResponse({"err": str(e)},status=400)

    else:
        return JsonResponse({"msg": "method not allowed"}, status=500)
