# Generated by Django 5.1.4 on 2024-12-31 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('youtube_url', models.URLField()),
                ('file_path', models.TextField()),
                ('duration', models.IntegerField()),
                ('thumbnail_url', models.URLField()),
                ('views', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
