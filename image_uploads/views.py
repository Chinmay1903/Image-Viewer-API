from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserImage
import openai
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

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
    #     if not image:
    #         return Response({"error": "Image file is required"}, status=400)
        
    #     user_image = UserImage.objects.create(user=user, image=image)
        
    #     try:
    #         analysis_result = self.analyze_image(user_image.image.file)  # Add image path
    #     except Exception as e:
    #         return Response({"error": f"Image analysis failed: {str(e)}"}, status=500)
        
    #     try:
    #         ai_description = self.generate_ai_description(analysis_result)
    #         user_image.description = ai_description
    #         user_image.save()
    #     except Exception as e:
    #         return Response({"error": f"AI description generation failed: {str(e)}"}, status=500)
        
    #     return Response({
    #         "message": "Image uploaded and analyzed successfully",
    #         "description": ai_description
    #     }, status=201)
    
    # def analyze_image(self, image_file):
    #     # Placeholder for actual image analysis (e.g., AWS Rekognition or Google Vision)
    #     # Example of using AWS Rekognition:
    #     rekognition_client = boto3.client('rekognition', 
    #                                       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #                                       region_name=settings.AWS_S3_REGION_NAME)

    #     try:
    #         image_file.seek(0)
    #         response = rekognition_client.detect_labels(
    #             Image={'Bytes': image_file.read()},
    #             MaxLabels=10,
    #             MinConfidence=75
    #         )
    #         labels = [label['Name'] for label in response['Labels']]
    #         return ", ".join(labels)
    #     except boto3.exceptions.NoCredentialsError:
    #         raise Exception("AWS credentials not found or invalid")
    #     except ClientError as e:
    #         raise Exception(f"Error analyzing image: {str(e)}")

    # def generate_ai_description(self, analysis_result):
    #     prompt = f"Generate a detailed and creative description based on this image analysis: {analysis_result}"
        
    #     # OpenAI API call to generate description
    #     response = openai.Completion.create(
    #         engine="gpt-3.5-turbo",
    #         prompt=prompt,
    #         max_tokens=100
    #     )

    #     description = response.choices[0].text.strip()
    #     return description
    
class UserImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Fetch all images associated with the logged-in user
        user_images = UserImage.objects.filter(user=user)
        
        # Prepare response data with image URLs
        images = [{"id": image.id, "url": image.image.url, "uploaded_at": image.uploaded_at, 'description': image.description} for image in user_images]
        
        return Response({"images": images}, status=200)
