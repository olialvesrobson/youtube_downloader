from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("video-downloader/", views.video_downloader, name="video_downloader"),
    path("handle-form/", views.video_downloader, name="handle_form"),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path("handle-form/", views.handle_form, name="handle_form"),
#     path("save-trimmed-video/", views.save_trimmed_video, name="save_trimmed_video"),
#     # path("save-transcript/", views.save_transcript, name="save_transcript"),
#     path("create-trimmed-video/", views.create_trimmed_video, name="create_trimmed_video"),
#     path("trim-existing-video/", views.trim_existing_video, name="trim_existing_video"),
    
# ]