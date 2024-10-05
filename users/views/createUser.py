from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from streaming_app_backend.mongo_client import users_collection


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
            return JsonResponse({"msg": "name is not present"},status=400)
        if not email:
            return JsonResponse({"msg": "email is not present"},status=400)
        if not password:
            return JsonResponse({"msg": "password is not present"},status=400)
        if not confirmPassword:
            return JsonResponse({"msg": "confirm password is not present"},status=400)
        if password != confirmPassword:
            return JsonResponse({"msg": "password and confirm password is not same"},status=400)
        
        userResponse = users_collection.insert_one(
            {"name":name,"email": email, "password": password,"loggedInBefore":False}
        )
        # userResponse["_id"]=str(userResponse["_id"])
        print(userResponse)
        if userResponse:
            return JsonResponse({"msg": "added user successfully", "success": True},status=201)
        else:
            return json(
                {"msg": "something went wrong while creating user ", "success": False},status=400
            )

    else:
        return JsonResponse({"msg": "wrong method"})
