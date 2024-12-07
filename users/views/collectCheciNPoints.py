from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import (
    dailyCheckInTask_collection,
    checkInPoints,
)
from bson import ObjectId
from .addPointsToProfile import addPointsToProfile

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
            print(taskIsPresent.get("_id"))
            taskPoints = checkInPoints.find_one(
                {"_id": ObjectId(taskIsPresent.get("assignedTaskId"))},
                {"allocatedPoints": 1},
            )
            print(taskPoints, "tp....")
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
