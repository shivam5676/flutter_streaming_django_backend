from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt



def questionUploader(request):
    
    if request.method == "POST":
        saved_files = []
        edu_videos = request.FILES.getlist(
            "eduVideos"
        )  # Use getlist to get multiple files
        

        # Define the storage location for the uploaded videos
        videos_directory = os.path.join(settings.MEDIA_ROOT, "education", "video")

        # Create the directory if it doesn't exist
        os.makedirs(videos_directory, exist_ok=True)

        fs = FileSystemStorage(
            location=videos_directory
        )  # Create subdirectory 'education/video'

        for video in edu_videos:
            try:
                # Attempt to save the video file
                filename = fs.save(video.name, video)  # Save file to media directory
                # Append the URL for the saved file
                file_url = os.path.join(
                    settings.MEDIA_URL, "education", "video", filename
                ).replace("\\", "/")
                saved_files.append({"url": file_url, "name": filename})
            except Exception as e:
                # Print the error message to the console
                print(f"Error saving file {video.name}: {str(e)}")
                return JsonResponse(
                    {"error": f"Error saving file {video.name}: {str(e)}"}, status=500
                )

        # If files are saved successfully, return the response
        return JsonResponse({"msg": "Files saved successfully", "files": saved_files})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
