from streaming_app_backend.mongo_client import videoPurchasedLogs
from bson import ObjectId


def checkPurchasedVideoData(videoId, userId):
    try:
        videoData = videoPurchasedLogs.find_one(
            {"shorts_Id": videoId, "user_Id": ObjectId(userId)}
        )
        print(videoData)
        if videoData:
            return True

        return False
    except Exception as err:
        raise ValueError("something went wrong in videoPurchasedLogs saving...{err}")
