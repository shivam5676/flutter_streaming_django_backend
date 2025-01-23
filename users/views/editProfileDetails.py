from django.http import JsonResponse
from streaming_app_backend.mongo_client import users_collection
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
@swagger_auto_schema(
    method="GET",
    operation_description="This API will give profile details to the user . We need to pass the token in the headers using the 'token' key.",
    manual_parameters=[
        openapi.Parameter(
            "token",  # The name of the header parameter
            openapi.IN_HEADER,  # Specifies that this is a header parameter
            description="User authentication token",  # Description for the header
            type=openapi.TYPE_STRING,  # Specifies that the type is a string
            required=True,  # Marks the token as required
        )
    ],
    responses={
        200: openapi.Response(description="trending shorts fetched successfully"),
        400: openapi.Response(description="Invalid request or token missing"),
        401: openapi.Response(description="Unauthorized - Invalid or missing token"),
        500: openapi.Response(description="method not allowed"),
    },
    tags=["User"],
)
@api_view(["GET"])

@csrf_exempt
def editProfileDetails(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            email = body.get("email")
            name = body.get("name")
            gender = body.get("gender")
            mobile = body.get("mobile")
            body = json.loads(request.body)
            userId = request.userId
            userDetails = users_collection.find_one_and_update(
                {"_id": ObjectId(userId)},
                {
                    "$set": {
                        "email": email,
                        "mobile": mobile,
                        "name": name,
                        "gender": gender,
                    }
                },
            )
            
            userDetails["_id"] = str(userDetails["_id"])
            return JsonResponse({"msg": "data updated successFully..."})
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"msg": "method not allowed"})
