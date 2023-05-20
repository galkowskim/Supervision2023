from django.urls import path
from .views import MainPageToDoList

urlpatterns = [
    path('', MainPageToDoList.as_view(), name='analyzer'),
]
