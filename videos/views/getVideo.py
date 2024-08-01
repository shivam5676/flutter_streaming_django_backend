from django.http import JsonResponse
from ..models import videoFiles
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getVideos(request):
    if request.method == "GET":
        excludedIds = request.session.get("userSession", [])
        videoFileResponse = (
            videoFiles.objects.exclude(id__in=excludedIds).order_by("?").values()[:10]
        )
        print(videoFileResponse)
        video_data = list(videoFileResponse)
        print(video_data)
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
