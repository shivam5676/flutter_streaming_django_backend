from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import (
    users_collection,
    checkInPoints,
    dailyCheckInTask_collection,
)
from datetime import datetime, timezone
from helper_function.saveUserInDataBase import saveUserInDataBase


@csrf_exempt
def createUser(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "Invalid JSON"}, status=400)
        email = body.get("email")
        name = body.get("name")
        password = body.get("password")
        confirmPassword = body.get("confirmPassword")
        if not name:
            return JsonResponse({"msg": "name is not present"}, status=400)
        if not email:
            return JsonResponse({"msg": "email is not present"}, status=400)
        if not password:
            return JsonResponse({"msg": "password is not present"}, status=400)
        if not confirmPassword:
            return JsonResponse({"msg": "confirm password is not present"}, status=400)
        if password != confirmPassword:
            return JsonResponse(
                {"msg": "password and confirm password is not same"}, status=400
            )
        try:
            userCreated = saveUserInDataBase(
                {"name": name, "email": email, "password": password}
            )
            return JsonResponse(
                {"msg": "added user successfully", "success": True}, status=201
            )
        except Exception as err:

            return JsonResponse(
                {"msg": str(err), "success": False},
                status=400,
            )

        # current_time = datetime.now(timezone.utc)
        # userResponse = users_collection.insert_one(
        #     {
        #         "name": name,
        #         "email": email,
        #         "password": password,
        #         "loggedInBefore": False,
        #         "gender": "null",
        #         "mobile": "null",
        #         "createdAt": current_time,  # created_at field
        #         "updatedAt": current_time,  # updated_at field
        #     }
        # )
        # user_id = userResponse.inserted_id
        # print("Inserted user ID:", user_id)
        # # userResponse["_id"]=str(userResponse["_id"])
        # print(userResponse, "userResponse")
        # if userResponse:
        #     checkInResponse = checkInPoints.find({}, {"_id": 1}).limit(7)
        #     allotedTask = []
        #     for index, checkInData in enumerate(checkInResponse):
        #         print(checkInData, "cdata")
        #         new_task = {
        #             "assignedTaskId": str(checkInData.get("_id")),
        #             "assignedUser": str(user_id),
        #             "status": "Pending" if index == 0 else "Alloted"
        #         }
        #         allotedTask.append(new_task)

        #     dailyAllocationResponse = dailyCheckInTask_collection.insert_many(allotedTask)
        #     if dailyAllocationResponse:
        #         users_collection.find_one_and_update(
        #             {"_id": user_id}, {"$set": {"assignedCheckInTask": 7}}
        #         )
        #     print(dailyAllocationResponse, "Dresponse........>")
        # return JsonResponse(
        #     {"msg": "added user successfully", "success": True}, status=201
        # )
        # else:
        #     return JsonResponse(
        #         {"msg": "something went wrong while creating user ", "success": False},
        #         status=400,
        #     )

    else:
        return JsonResponse({"msg": "wrong method"})
