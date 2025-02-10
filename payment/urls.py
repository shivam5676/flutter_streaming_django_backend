from django.urls import path
# from ..payment.paymentUrlGeneration import paymentUrlGeneration
from payment.paymentUrlGeneration import paymentUrlGeneration

urlpatterns = [
    path("getUrl/", paymentUrlGeneration),
]
