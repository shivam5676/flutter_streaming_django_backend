import jwt
from django.http import JsonResponse


def tokenCreator(data):

    try:
        print(data,"tilaaaaa")
        token = jwt.encode(data, "shivamssr", algorithm="HS256")
        print(token)
        #    token = token.decode('utf-8')
        #   print(token,"token")
        return token
    
    except Exception as e:
        print("error in token generation", e)
        raise ValueError(str("error in token generation"))
    #    return JsonResponse({"msg":"something went wrong"})
