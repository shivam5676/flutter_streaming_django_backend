from ..models import Slider
from django.http import JsonResponse
def getSlider(request):
    sliderData=Slider.objects.all()
    print(sliderData)
    return JsonResponse({"msg":"executed"})