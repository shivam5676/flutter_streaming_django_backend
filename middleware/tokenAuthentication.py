def accesstoken_authenticator(get_response):
    def middleware(request):
        response=get_response(request)
        
        return response
        
