from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Video
import os
import yt_dlp
from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import subprocess

def home(request):
    return render(request, "main.html")

def video_downloader(request):
    if request.method == "POST":
        # Extract form data
        youtube_url = request.POST.get("url")
        time_start_str = request.POST.get("time_start", "0:00")  # Default to "0:00"
        time_range = int(request.POST.get("time_range", 0))  # Default to full video (0)
        action = request.POST.get("action")  # Determine if it's "download" or "transcript"

        # Validate and convert start time from MM:SS to seconds
        try:
            minutes, seconds = map(int, time_start_str.split(":"))
            time_start = minutes * 60 + seconds
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid start time format. Use MM:SS."})

        # Calculate end time (start time + range), or set to None for full video
        time_end = time_start + time_range if time_range > 0 else None

        # Perform the requested action
        if action == "download":
            # Handle the video download
            return download_video_logic(youtube_url, time_start, time_end)
        elif action == "transcript":
            # Handle the transcript generation
            return fetch_transcript_logic(youtube_url, time_start, time_end)
        else:
            # Return an error for an invalid action
            return JsonResponse({"status": "error", "message": "Invalid action specified."})

    # For non-POST requests, render the form
    return render(request, "video_downloader.html")


def download_video_logic(youtube_url, time_start, time_end):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info.get("title")
            views = info.get("view_count")
            thumbnail = info.get("thumbnail")
            duration = info.get("duration")

        # Prepare download directory
        download_dir = os.path.join(settings.MEDIA_ROOT, "downloads")
        os.makedirs(download_dir, exist_ok=True)
        video_output_path = os.path.join(download_dir, f"{title}_downloaded.mp4")

        # yt-dlp download command
        yt_dlp_command = [
            "yt-dlp",
            youtube_url,
            "-o", video_output_path,
            "--merge-output-format", "mp4"
        ]

        # Execute download
        subprocess.run(yt_dlp_command, check=True)

        # Trim video if needed
        if time_end is not None:
            trimmed_output_path = os.path.join(download_dir, f"{title}_{time_start}_{time_end}_seconds.mp4")
            ffmpeg_command = [
                "ffmpeg",
                "-i", video_output_path,
                "-ss", str(time_start),
                "-to", str(time_end),
                "-c", "copy",
                trimmed_output_path
            ]
            subprocess.run(ffmpeg_command, check=True)
            video_output_path = trimmed_output_path

        # Save video details to the database
        video = Video.objects.create(
            title=title,
            youtube_url=youtube_url,
            file_path=os.path.relpath(video_output_path, settings.MEDIA_ROOT),
            duration=duration,
            thumbnail_url=thumbnail,
            views=views
        )

        relative_file_path = os.path.relpath(video_output_path, settings.MEDIA_ROOT)
        
        # Return JSON response
        return JsonResponse({
            "status": "success",
            "file": f"{settings.MEDIA_URL}{relative_file_path}",
            "title": video.title,
            "views": video.views,
            "thumbnail": video.thumbnail_url,
            "duration": video.duration
        })

    except subprocess.CalledProcessError as e:
        return JsonResponse({"status": "error", "message": f"Command failed: {e}"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})



# def download_video_logic(youtube_url):
#     try:
#         with yt_dlp.YoutubeDL() as ydl:
#             info = ydl.extract_info(youtube_url, download=False)
#             video = {
#                 "title": info.get("title"),
#                 "views": info.get("view_count"),
#                 "thumbnail_url": info.get("thumbnail"),
#                 "duration": info.get("duration"),
#                 "file_url": "/media/path/to/video.mp4"  # Adjust this path as needed
#             }
#         return video
#     except Exception as e:
#         return {"error": str(e)}


def fetch_transcript_logic(youtube_url, time_start, time_end):
    """
    Logic to fetch the transcript with specified start and end times.
    """
    try:
        # Extract video ID from the URL
        video_id = youtube_url.split("v=")[-1].split("&")[0]

        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Filter transcript based on time range
        filtered_transcript = transcript
        if time_end is not None:
            filtered_transcript = [
                item for item in transcript
                if time_start <= item["start"] < time_end
            ]

        # Format transcript with timestamps
        formatted_transcript = "\n".join(
            f"[{item['start']:.2f}] {item['text']}" for item in filtered_transcript
        )

        # Save the transcript to a file
        transcript_dir = os.path.join(settings.MEDIA_ROOT, "transcripts")
        os.makedirs(transcript_dir, exist_ok=True)
        transcript_file_path = os.path.join(transcript_dir, f"{video_id}_transcript.txt")

        with open(transcript_file_path, "w", encoding="utf-8") as file:
            file.write(formatted_transcript)

        # Return transcript information
        relative_file_path = os.path.relpath(transcript_file_path, settings.MEDIA_ROOT)
        return JsonResponse({
            "status": "success",
            "file": f"{settings.MEDIA_URL}{relative_file_path}",
            "transcript": formatted_transcript
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

