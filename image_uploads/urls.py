from django.urls import path
from .views import UploadImageView, UserImagesView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='image_upload'),
    path('get/', UserImagesView.as_view(), name='user_images')
]