from django.http import JsonResponse
from streaming_app_backend.mongo_client import (
    dailyCheckInTask_collection,
    checkInPoints,
)
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
@csrf_exempt
def dailyCheckInTask(request):
    if request.method == "POST":
        body = json.loads(request.body)
        userId = request.userId

        checkInTask = dailyCheckInTask_collection.find({"assignedUser": userId})
        if not checkInTask:
            return JsonResponse({"msg": "no task found"})
        taskList = []
        for task in checkInTask:

            checkInPointsData = checkInPoints.find_one(
                {"_id": ObjectId(task["assignedTaskId"])}, {"_id": 0}
            )
            if checkInPointsData:

                taskDetails = {
                    "taskId": str(task.get("_id")),
                    "status": task.get("status"),
                    **checkInPointsData,
                }
                taskList.append(taskDetails)

        return JsonResponse({"msg": "checkIn Called", "checkInTask": taskList})
