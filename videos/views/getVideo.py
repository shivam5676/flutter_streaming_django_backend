from django.http import JsonResponse
from ..models import videoFiles
from django.views.decorators.csrf import csrf_exempt
from ..models import adsVideos


@csrf_exempt
def getVideos(request):
    if request.method == "GET":
        print("Session ID:", request.COOKIES.get('sessionid'))
        print(request.headers)
        
        # return JsonResponse({"msg":"testing"})
        excludedIds = request.session.get("userSession", [])
        print(excludedIds,"ids")
        videoFileResponse = (
            videoFiles.objects.exclude(id__in=excludedIds).order_by("?").values()[:5]
        )
        
        video_data = list(videoFileResponse)
        if(len(video_data)>0):
            adsFileResponse = adsVideos.objects.order_by("?").values()[:1]
            ads_data = list(adsFileResponse)
            video_data.extend(ads_data)
        # print(videoFileResponse)
      
        # print(len(video_data) == 0)
        
        # video_data.extend(ads_data)
        # print(video_data)
        video_ids = (
            []
        )  # we wiil store all fetched ids here so that user could  not see the same content multiple times

        for video in video_data:
            video_ids.append(video["id"])
        if "userSession" in request.session:
            request.session["userSession"].extend(video_ids)
        else:
            request.session["userSession"] = video_ids
        request.session.modified = True
        request.session.save()

        print(video_ids)
        print(request.session)
        return JsonResponse({"data": video_data}, status=200)

        # responseVideofiles = videoFiles.objects.all().values(
        #     "id", "path", "userId", "cretaedAt"
        # )

        # # # Convert QuerySet to a list of dictionaries
        # data = list(responseVideofiles)

        # # Return JSON response with the data
        # return JsonResponse({"data": data}, status=200)
    else:
        return JsonResponse({"msg": "method not allowed"}, status=405)
