import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def convert_video_to_audio(video_name):
    # Extract file name without extension

    base_name = os.path.splitext(os.path.basename(video_name))[0]
    # print(base_name, "base")
    project_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "media", "education", "video"
        )
    )

    # Combine project directory with the relative path of the video
    video_path = os.path.join(project_dir, video_name)

    # Define the output audio path with the same name and .wav extension
    output_audio_path = f"media/education/videoAudio/{base_name}.wav"

    # Check if the audio file already exists
    if os.path.exists(output_audio_path):
        print(f"Audio file '{output_audio_path}' already exists. Skipping conversion.")
        return f"{base_name}.wav"
    print(video_path, "video path")
    # Load the video clip
    video = VideoFileClip(video_path)

    # Extract the audio and save it
    video.audio.write_audiofile(output_audio_path)
    print(base_name, "bbbbbbbbbbb")
    return f"{base_name}.wav"



def convert_audio_to_text(audio_file_path, output_file_path):
    # Initialize recognizer class (for recognizing the speech)
    if not os.path.exists(audio_file_path):
        print(f"File not found: {audio_file_path}")
        return None
    recognizer = sr.Recognizer()
    print(audio_file_path, "afile")
    print(output_file_path, "ofile")
    # Open the audio file
    with sr.AudioFile(audio_file_path) as source:
        # Listen to the audio file
        audio_data = recognizer.record(source)
        # Convert audio to text using Google's speech recognition
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")

            # Save the recognized text to a file
            with open(output_file_path, "w") as file:
                file.write(text)

            return text
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")


@csrf_exempt
def generate_response(request):
    # print("hello")
    videoFileAddress = json.loads(request.body)
    # print(videoFileAddress["file"]["url"],videoFileAddress["file"]["name"])
    videoLocation = videoFileAddress["file"]["url"]
    videoName = videoFileAddress["file"]["name"]
    print(videoLocation)
    # Convert video to audio

    audio_name = convert_video_to_audio(videoName)
    audio_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "media",
            "education",
          
            "videoAudio",
            audio_name,
        )
    )
    print(audio_path, "auuuusdhkshfrh")
    # Convert audio to text and save it
    fileTextPAth = os.path.join(settings.MEDIA_ROOT, "education", "videoText")
    outpuData = convert_audio_to_text(audio_path, f"{audio_path}.txt")
    return JsonResponse({"data": outpuData})
    # Remove the generated audio file after processing
    # try:
    #     os.remove(rf"{audio_path}")
    #     print(f"Audio file '{audio_path}' has been removed.")
    # except Exception as e:
    #     print(f"Error while trying to remove the audio file: {e}")


# generate_response(request,"...")
