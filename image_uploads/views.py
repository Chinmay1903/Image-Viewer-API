from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserImage

class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = request.user
        image = request.data.get('image')

        if image:
            user_image = UserImage.objects.create(user=user, image=image)
            return Response({"message": "Image uploaded successfully"}, status=201)

        return Response({"error": "Image file is required"}, status=400)
    
class UserImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Fetch all images associated with the logged-in user
        user_images = UserImage.objects.filter(user=user)
        
        # Prepare response data with image URLs
        images = [{"id": image.id, "url": image.image.url, "uploaded_at": image.uploaded_at} for image in user_images]
        
        return Response({"images": images}, status=200)
