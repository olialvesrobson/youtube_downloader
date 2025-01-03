from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    file_path = models.TextField()
    duration = models.IntegerField()
    thumbnail_url = models.URLField()
    views = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title