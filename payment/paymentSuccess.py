from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from streaming_app_backend.mongo_client import paidMintsBuyerCollection, client
from users.views.addPointsToProfile import addPointsToProfile


@csrf_exempt
def paymentSuccess(request):
   
    PAYU_KEY = "61Cs1H"
    PAYU_SALT = "L1CeWVdYlg8jVhJFxuSnB1TO8UgcjubF"
    txnid = request.POST.get("txnid")
    headers = {"key": PAYU_KEY, "command": "verify_payment"}
    mihpayid = request.POST.get("mihpayid") or ""
    bank_ref_num = request.POST.get("bank_ref_num") or ""

    paymentMode = request.POST.get("mode") or ""

    netAmountDeducted = request.POST.get("net_amount_debit") or ""
    paymentGateway = request.POST.get("PG_TYPE") or ""
    paymentAggregator = request.POST.get("pa_name") or ""

    try:
        session = client.start_session()
        session.start_transaction()
        # reqData = requests.post("https://test.payu.in/merchant/postservice.php?form=2")
        # print(reqData)
        paidMintsPlan = paidMintsBuyerCollection.find_one_and_update(
            {"txnid": txnid},
            {
                "$set": {
                    "status": "Success",
                    "mihpayid": mihpayid,
                    "Deductable_Amount": netAmountDeducted,
                    "paymentSource": "Payu",
                    "paymentMode": paymentMode,
                    "bank_ref_num": bank_ref_num,
                    "netAmountDeducted": netAmountDeducted,
                    "paymentGateway": paymentGateway,
                    "paymentAggregator": paymentAggregator,
                }
            },
            session=session,
        )

        addPointsToProfile(
            paidMintsPlan.get("userId"), paidMintsPlan.get("amount"), session
        )
        # for index, data in paidMintsPlan.items():
        #     print(index, "===>", data)
        session.commit_transaction()
        return JsonResponse(
            {
                "msg": "payment success",
            },
            status=200,
        )
    except Exception as err:
        # session.abort_transaction()
        return JsonResponse({"msg": str(err)}, status=400)
