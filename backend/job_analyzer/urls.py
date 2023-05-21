from django.urls import path

from .views import MainPageJobAdvertisementList, details, dashboard

urlpatterns = [
    path('', MainPageJobAdvertisementList.as_view(), name='main'),
    path('advertisement/<int:pk>/', details, name='advertisement'),
    path('dashboard/', dashboard, name='dashboard'),
]
