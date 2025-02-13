from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from streaming_app_backend.mongo_client import paidMintsBuyerCollection
from users.views.addPointsToProfile import addPointsToProfile


@csrf_exempt
def paymentSuccess(request):

    PAYU_KEY = "61Cs1H"
    PAYU_SALT = "L1CeWVdYlg8jVhJFxuSnB1TO8UgcjubF"
    txnid = request.POST.get("txnid")
    headers = {"key": PAYU_KEY, "command": "verify_payment"}
    mihpayid = request.POST.get("mihpayid")
    amount = request.POST.get("amount")
    try:
        # reqData = requests.post("https://test.payu.in/merchant/postservice.php?form=2")
        # print(reqData)
        paidMintsPlan = paidMintsBuyerCollection.find_one_and_update(
            {"txnid": txnid},
            {"$set": {"status": "Success", "mihpayid": mihpayid, "amount": amount}},
        )
        print(paidMintsPlan.get("userId"))
        addPointsToProfile(paidMintsPlan.get("userId"), paidMintsPlan.get("amount"))
        # for index, data in paidMintsPlan.items():
        #     print(index, "===>", data)

        return JsonResponse(
            {
                "msg": "payment success",
            },
            status=200,
        )
    except Exception as err:
        return JsonResponse({"msg": str(err)}, status=400)
