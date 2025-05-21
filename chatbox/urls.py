from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkview/', views.checkview, name='checkview'),
    path('<str:room_name>/', views.chatroom, name='chatroom'),
    path('send', views.send, name='send'),
    path('messages', views.getmsg, name='getmsg'),  
    path('messages/<str:room_name>/', views.fetch_messages, name='fetch_messages'),
]
