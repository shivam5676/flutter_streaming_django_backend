import hashlib
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    """Generate PayU Payment Request"""
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

            # ✅ Ensure all required parameters are included
            hash_data = {
                "key": PAYU_KEY,
                "txnid": txnid,
                "amount": amount,
                "productinfo": productinfo,
                "firstname": firstname,
                "email": email,
                "phone": phone,
                "surl": "http://192.168.1.64:8000/payment/success/",
                "furl": "https://192.168.1.64:8000yourdomain.com/payment/error/",
            }
            hash_data["hash"] = generate_hash(hash_data)

            return JsonResponse({"payu_url": PAYU_URL, "params": hash_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
