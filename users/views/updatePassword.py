from django.http import JsonResponse
from streaming_app_backend.mongo_client import forgotPasswordRequests, users_collection
from django.utils.timezone import now
from datetime import timedelta
from helper_function.passwordEncryption import passwordEncryption
import json
from bson import ObjectId
from helper_function.updatedPasswordConfirmation import updatedPasswordConfirmation


def updatePassword(request):
    body = json.loads(request.body)
    userId = request.userId
    passwordRequestId = request.otpId
    # passwordRequestId = body.get(
    #     "otpId"
    # )  # this is the requestId for getting already created otp log
    # print(passwordRequestId)
    # print(userId)
    if not passwordRequestId:
        return JsonResponse({"msg": "invalid password request id "}, status=400)

    password = body.get("password")
    confirmPassword = body.get("confirmPassword")
    if not password:
        return JsonResponse({"msg": "no password data found in request"}, status=400)
    if confirmPassword != password:
        return JsonResponse(
            {"msg": "password and confirm password are not same"}, status=400
        )
    try:
        fifteen_min_ago = now() - timedelta(minutes=15)
        existing_Requests = forgotPasswordRequests.find_one(
            {
                "isUsed": True,
                "_id": ObjectId(passwordRequestId),
                "userId": ObjectId(userId),
                "createdTime": {"$gte": fifteen_min_ago},
            },
            {"userId": 1},
        )
        print(existing_Requests)
        if not existing_Requests:
            return JsonResponse(
                {"msg": "No request found for changing otp in previous 15 minutes"},
                status=400,
            )
        hashedPassword = passwordEncryption(password)
        updatedPassword = users_collection.find_one_and_update(
            {
                "_id": ObjectId(userId),
            },
            {"$set": {"password": hashedPassword}},
            projection={"name": True, "email": True},
        )
        print(updatedPassword)
        updatedPasswordConfirmation(
            {"name": updatedPassword.get("name"), "email": updatedPassword.get("email")}
        )
        return JsonResponse({"msg": "Password Changed Successfully"}, status=200)
    except Exception as err:
        return JsonResponse({"msg": f"{err}"}, status=400)
