from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import videoFiles
from django.utils import timezone
@csrf_exempt
def upload(request):
    print("req is coming")
    if(request.method=="POST"):
        print(request.FILES)
        file= request.FILES.get("videos12345")
        user_id=1
        if file and user_id:
            video = videoFiles.objects.create(path=file, userId=user_id,createdAt=timezone.now())
            return JsonResponse({"msg":f"Uploaded: {video.path.url}"},status=200)
        else:
            return JsonResponse({"msg":"No file Found or userId missing"},status=400)
    else:
        return JsonResponse({"msg":"method not allowed"},status=405)
          