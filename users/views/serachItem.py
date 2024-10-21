from django.http import JsonResponse
from streaming_app_backend.mongo_client import movies_collection


def serachItem(request):
    if request.method == "GET":
        searchedItem = request.GET.get("name")
        if not searchedItem:
            return JsonResponse(
                {"msg": "searched item is invalid", "status": False}, status=404
            )
        # print(searchedItem)
        searchedResult = movies_collection.find(
            {"name": {"$regex": searchedItem, "$options": "i"}},
            {"_id": 1, "name": 1, "fileLocation": 1},
        )
        print(searchedResult)
        moviesList = []
        for data in searchedResult:
            print(data)
            data["_id"] = str(data.get("_id"))
            moviesList.append(data)
        if len(moviesList) == 0:
            return JsonResponse(
                {
                    "msg": "no data Found for serached Query",
                    "data": moviesList,
                    "success": False,
                },
                status=200,
            )
        return JsonResponse(
            {"msg": "got it", "data": moviesList, "success": False}, status=200
        )
    else:
        return JsonResponse({"msg": "wrong method", })
