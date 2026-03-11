from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('reset/',views.reset,name='reset'),
    path('chat/',views.chat,name='chat'),
]