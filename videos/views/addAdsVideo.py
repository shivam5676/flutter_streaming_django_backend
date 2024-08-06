from django.http import JsonResponse
from ..models import adsVideos
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def addAdsVideo(request):
    if request.method == "POST":
        print(request.FILES)
        file = request.FILES.get("adVideo12345")
        userId = 1
        if file and userId:
            adVideoAddedResponse = adsVideos.objects.create(
                path=file, userId=userId, createdAt=timezone.now()
            )
            return JsonResponse({"msg": "ads video successfullyAdded "})
        else:
            return JsonResponse({"msg": "File or userId is missing"}, status=400)
    return JsonResponse({"msg": "Invalid request method"}, status=405)
