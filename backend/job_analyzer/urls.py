from django.urls import path

from .views import MainPageJobAdvertisementList, details, update_fake_status, dashboard

urlpatterns = [
    path('', MainPageJobAdvertisementList.as_view(), name='main'),
    path('advertisement/<int:pk>/', details, name='advertisement'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update_fake_status/', update_fake_status, name='update_fake_status')
]
