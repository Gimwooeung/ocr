from django.urls import path
from ocr.views import upload_image

urlpatterns = [
    path('', upload_image, name='upload_image'),
]