from django.urls import path

from .views import JobAdvertisementDetail, MainPageJobAdvertisementList

urlpatterns = [
    path('', MainPageJobAdvertisementList.as_view(), name='main'),
    path('advertisement/<int:pk>/',
         JobAdvertisementDetail.as_view(), name='advertisement'),
]
