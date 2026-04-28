from django.urls import path
from .views import guest_list

urlpatterns = [
    path('', guest_list),
]