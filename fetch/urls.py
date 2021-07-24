from django.urls import path
from .views import *

urlpatterns = [
    path('acc', FetchAcc.as_view()),
    path('user', FetchUser.as_view()),
    path('contact', FetchCt.as_view()),
]
