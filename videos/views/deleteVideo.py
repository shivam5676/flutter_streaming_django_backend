from django.http import JsonResponse
from ..models import videoFiles
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
# @require_http_methods(["POST"])
def deleteVideo(request):

    if request.method == "POST":
        body = json.loads(request.body)
        id = body.get("id")
        if not id:
            return JsonResponse({"msg": "no id present"}, status=400)
        userId = 1
        try:

            video = videoFiles.objects.get(id=id, userId=userId)
            video.path.delete(save=False)
            video.delete()
            return JsonResponse({"msg": "data deleted successfully"}, status=200)
        except videoFiles.DoesNotExist:
            return JsonResponse({"msg":"Video does not exist"},status=400)

    else:

        return JsonResponse({"msg": "method not allowed"})
