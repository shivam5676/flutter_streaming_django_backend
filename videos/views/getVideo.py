from django.http import JsonResponse
from ..models import videoFiles
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getVideos(request):
    responseVideofiles = videoFiles.objects.all().values('path', 'userId', 'createdAt')
    
    # Convert QuerySet to a list of dictionaries
    data = list(responseVideofiles)
    
    # Return JSON response with the data
    return JsonResponse({"data": data})