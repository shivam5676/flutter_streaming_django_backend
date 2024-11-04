from streaming_app_backend.mongo_client import users_collection
from bson import ObjectId

def addPointsToProfile(userId, allotedPoints):
    try:
        # Perform the update with increment and create if not exist (upsert)
        updateUser = users_collection.update_one(
            {"_id": ObjectId(userId)},  # Ensure userId is an ObjectId
            {"$inc": {"allocatedPoints": allotedPoints}},  # Increment or initialize allocatedPoints
            upsert=True  # Insert a new document if none matches
        )
        
        # Check if the update was successful
        if updateUser.acknowledged:
            return {"success": True, "data": updateUser.raw_result}
        else:
            return {"success": False, "error": "Failed to update points."}
    except Exception as e:
        return {"success": False, "error": str(e)}
