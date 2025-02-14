from django.urls import path

# from ..payment.paymentUrlGeneration import paymentUrlGeneration
from payment.paymentUrlGeneration import paymentUrlGeneration
from payment.paymentError import paymentError
from payment.paymentSuccess import paymentSuccess
from payment.verifyPayment import verifyPayment

urlpatterns = [
    path("getUrl/", paymentUrlGeneration),
    path("error/", paymentError),
    path("success/", paymentSuccess),
    path("verify/", verifyPayment),
]
