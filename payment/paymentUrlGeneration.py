import hashlib
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from streaming_app_backend.mongo_client import paidMintsBuyerCollection, client
from datetime import datetime

# ✅ Use Correct Test Credentials
PAYU_KEY = "61Cs1H"
PAYU_SALT = "L1CeWVdYlg8jVhJFxuSnB1TO8UgcjubF"
PAYU_URL = "https://test.payu.in/_payment"


def generate_hash(data):
    """Generate PayU hash using SHA-512 with the correct parameter sequence"""
    hash_string = f"{PAYU_KEY}|{data['txnid']}|{data['amount']}|{data['productinfo']}|{data['firstname']}|{data['email']}|||||||||||{PAYU_SALT}"
    return hashlib.sha512(hash_string.encode()).hexdigest()


@csrf_exempt
def paymentUrlGeneration(request):
    # """Generate PayU Payment Request"""

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            print(data)
            txnid = data.get("txnid")  # Unique transaction ID
            amount = data.get("amount")
            email = data.get("email")
            phone = data.get("phone")
            firstname = data.get("firstname")
            productinfo = data.get("productinfo") or "not provided"
            userId = request.userId
            # ✅ Ensure all required parameters are included
            if not txnid:
                print(txnid)
                return JsonResponse({"msg": "invalid txn id"}, status=400)
            if not amount:
                print(amount)
                return JsonResponse({"msg": "invalid amount"}, status=400)
            hash_data = {
                "key": PAYU_KEY,
                "txnid": txnid,
                "amount": amount,
                "productinfo": productinfo,
                "firstname": firstname,
                "email": email,
                "phone": phone,
                "surl": "http://192.168.1.62:8000/payment/success/",
                "furl": "https://192.168.1.62:8000yourdomain.com/payment/error/",
            }
            hash_data["hash"] = generate_hash(hash_data)
            try:
                paidMintsBuyerCollection.insert_one(
                    {
                        "userId": userId,
                        "txnid": txnid,
                        "amount": amount,
                        "date": datetime.now(),
                        "status": "Pending",
                        "couponApplied": "test100",
                        
                    },
                )
                return JsonResponse(
                    {"payu_url": PAYU_URL, "params": hash_data}, status=200
                )
            except Exception as err:
                print(err)
                raise ValueError("err while saving transaction data in database")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
