# YouTube Downloader - Django Project

This is a Python Django-based web application designed to provide users with an intuitive interface to download videos from YouTube and manage them effectively. The project is modular, with clear separation of concerns for templates, views, and static files.

## Features

- Download videos from YouTube using a simple interface.
- Generate video transcripts if available.
- View downloaded videos with options for trimming and managing.
- Responsive design for seamless usage across devices.

## Screenshots

### Home Page
The home page provides an overview of the application and a link to the video downloader feature.

![Home Page](downloader/static/images/Screenshot%20home.png)

### Video Downloader Page
This page allows users to input a YouTube URL, select start time, specify a range, and choose to either download the video or fetch its transcript.

![Home Page](downloader/static/images/Screenshot%20video-downloader.png)


## Installation

### Prerequisites
- Python 3.10 or above
- Django 5.1
- A virtual environment tool (e.g., `venv` or `virtualenv`)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repository/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**
   Apply migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   Start the server to view the application:
   ```bash
   python manage.py runserver
   ```

   Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure

```
├── downloader
│   ├── static
│   │   ├── images
│   │   │   ├── Screenshot home.png
│   │   │   ├── Screenshot downloader video.png
│   │   └── globalstyles.css
│   ├── templates
│   │   ├── master.html
│   │   ├── main.html
│   │   ├── video_downloader.html
│   │   └── container_video.html
│   ├── views.py
│   └── urls.py
├── youtube_downloader
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── manage.py
```

## Usage

### Home Page
- Navigate to the home page to get started.
- Click the **Video Downloader** link to access the main functionality.

### Video Downloader
- Enter a YouTube URL.
- Specify the start time (in MM:SS format) and duration (in seconds).
- Select an action:
  - **Download Video**: Download the specified video segment.
  - **Fetch Transcript**: Generate a transcript if available.

### Viewing Videos
- View downloaded videos with options to preview, trim, and save locally.


