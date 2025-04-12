from django.http import JsonResponse
from streaming_app_backend.mongo_client import (
    users_collection,
    movies_collection,
    continueWatching,
)
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="POST",
    operation_description="This API allows the user to save shorts watch history details. The request should contain the user token in headers and an array of selected genres in the body.",
    manual_parameters=[
        openapi.Parameter(
            "token",  # The name of the header parameter
            openapi.IN_HEADER,  # Specifies that this is a header parameter
            description="User authentication token",  # Description of the token
            type=openapi.TYPE_STRING,  # Specifies that the type is a string
            required=True,  # Marks the token as required
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "moviesId": openapi.Schema(
                type=openapi.TYPE_STRING, description="Movie Id"
            ),
            "currentShortsId": openapi.Schema(
                type=openapi.TYPE_STRING, description="Current Short Id"
            ),
            "timestamp": openapi.Schema(
                type=openapi.TYPE_STRING, description="Timestamp"
            ),
        },
        required=["moviesId", "currentShortsId", "timestamp"],
    ),
    responses={
        200: openapi.Response(description="history updated successfully"),
        400: openapi.Response(description="Invalid request or token missing"),
        401: openapi.Response(description="Unauthorized - Invalid or missing token"),
        500: openapi.Response(description="method not allowed"),
    },
    tags=["User"],
)
@api_view(["POST"])
@csrf_exempt
def continueWatchingHistorySaving(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            moviesId = body.get("moviesId")
            currentShortsId = body.get("currentShortsId")
            timestamp = body.get("timestamp")
            userId = request.userId

            if not userId:
                return JsonResponse({"msg": "userId is missing"}, status=400)
            elif not moviesId:
                return JsonResponse({"msg": "moviesId is missing"}, status=400)
            elif not currentShortsId:
                return JsonResponse({"msg": "currentShortsId is missing"}, status=400)
            elif not timestamp:
                return JsonResponse({"msg": "timestamp is missing"}, status=400)

            userDetails = users_collection.find_one(
                {"_id": ObjectId(userId)},
                {"password": 0},
            )
            if not userDetails:
                return JsonResponse({"msg": "no user found"}, status=400)
            # if(not ObjectId())
            
            # if not isinstance(currentShortsId):
            #     currentShortsId=ObjectId(currentShortsId)
            movieDetails = movies_collection.find_one(
                {
                    "_id": ObjectId(moviesId),
                    "shorts": currentShortsId,
                    # Directly match the ObjectId in the array
                }
            )
            print(movieDetails)
            if not movieDetails:
                return JsonResponse(
                    {"msg": "no movie found or short not found"}, status=400
                )

            result = continueWatching.update_one(
                {"userId": userId, "moviesId": moviesId},
                {
                    "$set": {
                        "currentShortsId": currentShortsId,
                        "timestamp": timestamp,
                    }
                },
                upsert=True,
            )
            if result.matched_count == 0:
                return JsonResponse(
                    {"msg": "History inserted successFully..."}, status=200
                )
            elif result.modified_count > 0:
                return JsonResponse(
                    {"msg": "History updated successfully..."}, status=200
                )
            else:
                return JsonResponse(
                    {
                        "msg": "No changes were necessary; history is up-to-date. (Document existed but no modification occurred (possibly already updated with the same values))"
                    },
                    status=200,
                )
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)

    else:
        return JsonResponse({"msg": "method not allowed"}, status=500)
