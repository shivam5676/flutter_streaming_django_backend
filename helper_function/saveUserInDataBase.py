from streaming_app_backend.mongo_client import (
    users_collection,
    checkInPoints,
    dailyCheckInTask_collection,
)
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta


def saveUserInDataBase(data):
   
    try:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        current_time = datetime.now(timezone.utc)

        today = datetime.today()

        # Add 7 days to today's date
        new_date = today + timedelta(days=7)
        next_allocation = new_date.strftime("%d/%m/%Y")
        userResponse = users_collection.insert_one(
            {
                "name": name,
                "email": email,
                "password": password,
                "loggedInBefore": False,
                "gender": "null",
                "mobile": "null",
                "createdAt": current_time,  # created_at field
                "updatedAt": current_time,  # updated_at field
                "next_Allocation": next_allocation,
            }
        )
        user_id = userResponse.inserted_id

        # userResponse["_id"]=str(userResponse["_id"])

        if userResponse:
            checkInResponse = checkInPoints.find({}, {"_id": 1}).limit(7)
            allotedTask = []
            for index, checkInData in enumerate(checkInResponse):
                print(checkInData, "cdata")
                new_task = {
                    "assignedTaskId": str(checkInData.get("_id")),
                    "assignedUser": str(user_id),
                    "status": "Pending" if index == 0 else "Alloted",
                }
                allotedTask.append(new_task)
            if allotedTask:
                dailyAllocationResponse = dailyCheckInTask_collection.insert_many(
                    allotedTask
                )
                if dailyAllocationResponse:
                    users_collection.find_one_and_update(
                        {"_id": user_id}, {"$set": {"assignedCheckInTask": 7}}
                    )

                return userResponse

        else:
            print("no user response")
            raise ValueError(" something went wrong while creating user")

    except Exception as err:
        print(err)
        raise ValueError((err))
