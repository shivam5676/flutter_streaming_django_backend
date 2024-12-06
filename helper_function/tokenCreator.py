import jwt
from django.http import JsonResponse
def tokenCreator(data):
     
     try:
        token=jwt.encode(data,"shivamssr")
     #    token = token.decode('utf-8')
        print(token,"token")
        return token  
     except Exception as e:
          print("hjdfhjrsg",e)
     #    return JsonResponse({"msg":"something went wrong"})
     
