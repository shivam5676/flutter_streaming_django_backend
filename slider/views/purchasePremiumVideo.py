from streaming_app_backend.mongo_client import (
    videoPurchasedLogs,
    users_collection,
    shorts_collection,
    client,
)
from django.http import JsonResponse
from bson import ObjectId
import json
from users.views.checkSignedVideo import checkSignedVideo
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def purchasePremiumVideo(request):
    if request.method == "POST":

        userId = request.userId

        session = client.start_session()
        session.start_transaction()
        try:
            print("hello")
            bodyData = json.loads(request.body)

            currentShortsID = bodyData.get("shortsID")
            print("shortsData")
            # verify video is exist or not in database
            shortsData = shorts_collection.find_one(
                {"_id": ObjectId(currentShortsID)}, session=session
            )
            print(shortsData)
            if not shortsData:
                session.abort_transaction()
                return JsonResponse({"err": "Invalid shorts Id"})
            videosPointsSpend = shortsData.get("purchasePoints") or 1
            purchaseThisShorts = videoPurchasedLogs.insert_one(
                {
                    "shorts_Id": currentShortsID,
                    "user_Id": (userId),
                },
                session=session,
            )
            if not purchaseThisShorts.acknowledged:
                session.abort_transaction()
                return JsonResponse(
                    {
                        "err": "unable to purchase the shorts... please try again or contact the customer support team "
                    }
                )
            print(userId)    
            user = users_collection.find_one(
                {"_id": ObjectId(userId)}, {"allocatedPoints": 1}, session=session
            )
            if not user:
                session.abort_transaction()
                return JsonResponse(
                    {"err": "unable to find the user with the given user id "}
                )
            userWalletPoints = user.get("allocatedPoints") or 0
            if userWalletPoints < videosPointsSpend:
                session.abort_transaction()
                return JsonResponse(
                    {
                        "msg": "Not enough mints to purchase this video ...please purchase some mints then try to unlock this Paid features"
                    },
                )
            updateAllocationPoints = users_collection.update_one(
                {"_id": ObjectId(userId)},
                {"$inc": {"allocatedPoints": -videosPointsSpend}},
                session=session,
            )
            print("start",updateAllocationPoints,"up.............",videosPointsSpend)
            if  updateAllocationPoints.modified_count == 0:
                session.abort_transaction()
                return JsonResponse(
                    {
                        "err": "problem while updating the allocating points after purchasing the video"
                    }
                )
            session.commit_transaction()
            return JsonResponse(
                {
                    "medium": checkSignedVideo(shortsData.get("medium")),
                    "high": checkSignedVideo(shortsData.get("high")),
                }
            )
        except Exception as err:
            session.abort_transaction()
            return JsonResponse({"err": str(err)}, status=400)
        finally:
            session.end_session()
    else:
        return JsonResponse({"msg": "Method not allowed"}, status=500)
