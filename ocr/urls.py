from django.urls import path
from ocr.views import upload_image
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('upload/', views.upload_image_chat_api, name='upload_image'),
    path('chat/', views.chat_view, name='chat_view'),
]