from django.urls import path
from .views import ChatSessionView, ChatSessionMessageView

urlpatterns = [
    path('sessions/', ChatSessionView.as_view(), name='create_chat'),
    path('sessions/<str:uri>/', ChatSessionView.as_view(), name='join_chat'),
    path('sessions/<str:uri>/messages/', ChatSessionMessageView.as_view(), name='chat_messages'),
]
