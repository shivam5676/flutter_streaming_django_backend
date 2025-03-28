from streaming_app_backend.mongo_client import videoPurchasedLogs
from bson import ObjectId


def checkPurchasedVideoData(videoId, userId):
    try:
        videoData = videoPurchasedLogs.find_one(
            {"shorts_Id": str(videoId), "user_Id": str(userId)}
        )

        print(videoData, videoId, userId)
        if videoData:
            return True

        return False
    except Exception as err:
        raise ValueError("something went wrong in videoPurchasedLogs checking...{err}")
