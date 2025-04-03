# This is the correct middleware structure
import jwt
import json
from django.http import JsonResponse
import os
from dotenv import load_dotenv


def access_token_authenticator(get_response):
    # This is the actual middleware function
    def accesstokenAuthMiddleware(request):
        print("request", request.headers)
        # print("Inside the middleware",jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3M2M1NDA2NzcwMTRjMTMzNDlhMzdhNCJ9.wo_uoHy_WB3ZLPZNr9dCuEZ_CAbYvYviRKSVdBafVk0","shivamssr", algorithms=["HS256"]))
        # Process request here, for example, token authentication
        excluded_paths = [
            "/check/",
            "/payment/success/",
            "/payment/error/",
            "/user/signIn/",
            "/user/register/",
            "/user/googleAuth/",
            "/user/googleAuth",
            "/allotement/",
            "/swagger/",  # Exclude Swagger documentation path
            "/swagger-ui/",  # Another potential Swagger UI path
            "/redoc/",  # If you're using Redoc for API docs
            "/swagger.json",  # If you have a Swagger JSON endpoint
            "/swagger.yaml",  # If you have a Swagger YAML endpoint
        ]  # Add paths to exclude here

        # Check if the request path is in the excluded list
        if request.path in excluded_paths:
            return get_response(request)

        # if request.body:  # Check if body is not empty
        #     try:

        #         body_data = json.loads(request.body)
        #         print(body_data, "Body data")  # Log body data (optional)
        #     except Exception as err:
        #         print(err)

        token = request.headers.get("token")

        if not token:

            return JsonResponse({"msg": "token not present"}, status=400)
        try:
            # print(os.getenv("sugarValue"),"lllodkshdhs")
            # Attempt to decode the token using the secret and algorithm
            decodedToken = jwt.decode(
                token, os.getenv("sugarValue"), algorithms=["HS256"]
            )
            # You can print or log the decoded token here

            request.userId = decodedToken.get("id")

        except jwt.ExpiredSignatureError:
            # Token has expired
            return JsonResponse({"msg": "Token has expired"}, status=400)
        except jwt.InvalidTokenError:
            # Token is invalid for other reasons
            return JsonResponse({"msg": "Invalid token"}, status=400)

        except Exception as e:
            # General exception for any other errors during decoding

            return JsonResponse(
                {"msg": "Something went wrong", "error": str(e)}, status=500
            )
        response = get_response(request)  # Pass the request to the next middleware/view

        return response

    return accesstokenAuthMiddleware  # Return the middleware function
