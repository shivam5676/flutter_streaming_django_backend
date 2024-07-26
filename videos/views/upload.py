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
            video = videoFiles.objects.create(path=file, userId=user_id,cretaedAt=timezone.now())
            # return HttpResponse(f"Upload started: {video.path.url}")
        else:
            return HttpResponse("No file uploaded or userId missing", status=400)
        
    return HttpResponse("upload started")