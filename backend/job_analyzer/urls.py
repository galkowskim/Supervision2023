from django.urls import path

from .views import MainPageJobAdvertisementList, details

urlpatterns = [
    path('', MainPageJobAdvertisementList.as_view(), name='main'),
    path('advertisement/<int:pk>/', details, name='advertisement'),
]
