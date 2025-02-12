from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def paymentError(request):
    return JsonResponse({"msg":"payment error"},status=400)