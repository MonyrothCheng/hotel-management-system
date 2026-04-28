from django.urls import path
from .views import booking_list

urlpatterns = [
    path('', booking_list),
]