from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import (
    dailyCheckInTask_collection,
    checkInPoints,
)
from bson import ObjectId
from .addPointsToProfile import addPointsToProfile


from drf_yasg import openapi
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="POST",
    operation_description="This API allows the user to collect check in task. The request should contain the user token in headers and an array of selected genres in the body.",
    manual_parameters=[
        openapi.Parameter(
            "token",  # The name of the header parameter
            openapi.IN_HEADER,  # Specifies that this is a header parameter
            description="User authentication token",  # Description of the token
            type=openapi.TYPE_STRING,  # Specifies that the type is a string
            required=True,  # Marks the token as required
        )
    ],request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "taskId": openapi.Schema(type=openapi.TYPE_STRING, description="current task id which you want to collect"),
           
        },
        required=["taskId"],
    ),
    responses={
        200: openapi.Response(description="task id retrieved successfully"),
        400: openapi.Response(description="Invalid request or token missing"),
        401: openapi.Response(description="Unauthorized - Invalid or missing token"),
        500: openapi.Response(description="method not allowed"),
    },
    tags=["User"],
)
@api_view(["POST"])
# i need to create a cron job for daliy allocating task
# i need to add a cron job for auto detecting its assigning datye and after seven days i need to add it in missed if i dont collect it(we can use alloatedDate so that we could verify when that points is allocated )
@csrf_exempt
def collectCheckInPoint(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON format"}, status=400)

        taskId = body.get("taskId")
        userId = request.userId
      
        if not taskId:
            return JsonResponse({"msg": "No Task Id Is present"}, status=404)

        # Try to update the task status to "Completed"
        taskIsPresent = dailyCheckInTask_collection.find_one_and_update(
            {"_id": ObjectId(taskId), "assignedUser": userId, "status": "Pending"},
            {"$set": {"status": "Completed"}},
        )
        # print(taskIsPresent)
        if taskIsPresent:
        
            taskPoints = checkInPoints.find_one(
                {"_id": ObjectId(taskIsPresent.get("assignedTaskId"))},
                {"allocatedPoints": 1},
            )
           
            if taskPoints:
                addPointsToProfile(userId,taskPoints.get("allocatedPoints"))
                return JsonResponse(
                    {
                        "msg": "Task completed successfully",
                        "allocatedPoints": taskPoints.get("allocatedPoints"),
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {"msg": "Points data not found for this task"}, status=404
                )

        else:
            return JsonResponse(
                {"msg": "No task found or task already completed"}, status=404
            )

    return JsonResponse({"msg": "Invalid request method"}, status=405)
