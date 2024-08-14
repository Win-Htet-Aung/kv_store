from django.urls import path
from .views import item_view


urlpatterns = [
    path("", item_view),
]
