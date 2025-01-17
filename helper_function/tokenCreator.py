import jwt
from django.http import JsonResponse


def tokenCreator(data):

    try:
        token = jwt.encode(data, "shivamssr", algorithm="HS256")
        #    token = token.decode('utf-8')
        #   print(token,"token")
        return token
    except Exception as e:
        print("error in token generation", e)
    #    return JsonResponse({"msg":"something went wrong"})
