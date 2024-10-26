from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import dailyCheckInTask_collection, checkInPoints
from bson import ObjectId

@csrf_exempt
def collectCheckInPoint(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON format"}, status=400)

        taskId = body.get("taskId")
        userId = body.get("userId")

        if not taskId:
            return JsonResponse({"msg": "No Task Id Is present"}, status=404)

        # Try to update the task status to "Completed"
        taskIsPresent = dailyCheckInTask_collection.find_one_and_update(
            {"assignedTaskId": taskId, "assignedUser": userId, "status": "Pending"},
            {"$set": {"status": "Completed"}}
        )

        if taskIsPresent:
            taskPoints = checkInPoints.find_one({"_id": ObjectId(taskId)}, {"allocatedPoints": 1})
            if taskPoints:
                return JsonResponse({
                    "msg": "Task completed successfully",
                    "allocatedPoints": taskPoints.get("allocatedPoints")
                }, status=200)
            else:
                return JsonResponse({"msg": "Points data not found for this task"}, status=404)
        
        else:
            return JsonResponse({"msg": "No task found or task already completed"}, status=404)

    return JsonResponse({"msg": "Invalid request method"}, status=405)
