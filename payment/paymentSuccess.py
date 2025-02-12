from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
@csrf_exempt
def paymentSuccess(request):
    headers={
        "key":"","command":"verify_payment"
    }
    try:
        reqData=requests.post("https://test.payu.in/merchant/postservice.php?form=2")
        print(reqData)
        
    except:
     return JsonResponse({"msg":"payment success"},status=200)