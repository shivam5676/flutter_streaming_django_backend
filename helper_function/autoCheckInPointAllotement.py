from streaming_app_backend.mongo_client import users_collection
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta


def autoCheckInPointAllotement(request):
    current_date = datetime.today().strftime("%d/%m/%Y")
    try:
        users_collection.find()
        print(current_date)

    except Exception as err:
        return JsonResponse({"msg": err})
