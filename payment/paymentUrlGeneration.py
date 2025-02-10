import hashlib
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ✅ Use Correct Test Credentials
PAYU_KEY = "LOz08k"
PAYU_SALT = "hyW3KX2FIDeb9biTaqRj8QHKIkeMuOCj"
PAYU_URL = "https://secure.payu.in/_payment"


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
            txnid = data.get("txnid")  # Unique transaction ID
            amount = data.get("amount")
            email = data.get("email")
            phone = data.get("phone")
            firstname = data.get("firstname")
            productinfo = "Test Product"

            # ✅ Ensure all required parameters are included
            hash_data = {
                "key": PAYU_KEY,
                "txnid": txnid,
                "amount": amount,
                "productinfo": productinfo,
                "firstname": firstname,
                "email": email,
                "phone": phone,
                "surl": "https://yourdomain.com/payment-success/",
                "furl": "https://yourdomain.com/payment-failure/",
            }
            hash_data["hash"] = generate_hash(hash_data)

            return JsonResponse({"payu_url": PAYU_URL, "params": hash_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
