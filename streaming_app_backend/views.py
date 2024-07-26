

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def testing(request):
    return JsonResponse({"msg":"testing successful"})