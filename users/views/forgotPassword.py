from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from streaming_app_backend.mongo_client import forgotPasswordRequests
import json


def forgotPassword(request):
    if request.method != "POST":
        return JsonResponse({"msg": "Invalid request method"}, status=405)

    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        user_id = request.userId  # Extract userId from request body

        if not user_id:
            return JsonResponse({"msg": "User ID is required"}, status=400)

        # Check if a request was already made within the last minute
        one_min_ago = now() - timedelta(minutes=1)
        existing_request = forgotPasswordRequests.find_one(
            {"userId": user_id, "createdTime": {"$gte": one_min_ago}}
        )

        if existing_request:
            return JsonResponse(
                {"msg": "Please wait before requesting again"}, status=429
            )

        # Insert new request log
        forgotPasswordRequests.insert_one({"userId": user_id, "createdTime": now()})

        return JsonResponse({"msg": "Password reset request logged successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"msg": "Invalid JSON format"}, status=400)
    except Exception as err:
        return JsonResponse({"msg": f"Error: {str(err)}"}, status=500)
