import jwt
from django.http import JsonResponse


def tokenCreator(data):

    try:

        token = jwt.encode(data, "shivamssr", algorithm="HS256")

        return token

    except Exception as e:
       
        raise ValueError(str("error in token generation"))
    #    return JsonResponse({"msg":"something went wrong"})
