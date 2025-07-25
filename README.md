# SlickMajic Multi-User Blueprint Architecture

This project is a Flask-based web application for generating videos with subtitles, images, and audio, supporting multi-user request queuing and processing. It integrates video editing, image generation, and script refinement, and uses a database to track user requests and video generation status.

## Features

- **REST API** for video and image generation
- **Multi-user request queue** to handle concurrent requests
- **Script refinement** and prompt generation
- **Automated image generation** based on script intent
- **Video creation** with audio, subtitles, and effects
- **Database integration** for user and video tracking
- **Environment configuration** via `.env` file

## Project Structure

```
.
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (DB path, API keys, etc.)
├── instance/
│   └── database.db               # SQLite database file
├── mainapp/
│   ├── __init__.py               # Flask app factory and blueprint registration
│   ├── model/
│   │   ├── database.py           # SQLAlchemy models (User, etc.)
│   │   ├── image_generation.py   # Image generation logic
│   │   └── scripts_generation.py # Script refinement and prompt logic
│   ├── multi_users_process/
│   │   └── queue_process.py      # Request queue for multi-user support
│   ├── routes/
│   │   └── image_generate.py     # API route for image/video generation
│   ├── video_editting/
│   │   └── creatomate.py         # Video editing, merging, and subtitle generation
│   └── video_generation/
│       └── Run_app.py            # Orchestrates the video generation pipeline
└── env/                          # Python virtual environment
```

## Setup

1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   Create a `.env` file in the root directory with content like:
   ```
   DATABASE_PATH=sqlite:///instance/database.db
   URL=your_api_url
   api_key=your_api_key
   ```

5. **Run the application**
   ```sh
   python main.py
   ```

## API Endpoints

- `POST /generate`  
  Queue a new video/image generation request.  
  **Body:**  
  ```json
  {
    "user_id": "...",
    "video_id": "...",
    "script": "...",
    "setting": "...",
    "aspect_ratio": "...",
    "theme": "...",
    "font_family": "...",
    "font_size": "...",
    "transcript_effect": "...",
    "stroke_color": "...",
    "font_weight": "...",
    "fill_color": "...",
    "max_length": ... 
  }
  ```

## Main Components

- [`main.py`](main.py): Starts the Flask app and initializes the database.
- [`mainapp/__init__.py`](mainapp/__init__.py): App factory, blueprint registration.
- [`mainapp/routes/image_generate.py`](mainapp/routes/image_generate.py): Handles `/generate` requests, manages queue and DB.
- [`mainapp/model/database.py`](mainapp/model/database.py): SQLAlchemy models and DB setup.
- [`mainapp/model/image_generation.py`](mainapp/model/image_generation.py): Image generation logic.
- [`mainapp/model/scripts_generation.py`](mainapp/model/scripts_generation.py): Script refinement and prompt extraction.
- [`mainapp/multi_users_process/queue_process.py`](mainapp/multi_users_process/queue_process.py): In-memory request queue.
- [`mainapp/video_editting/creatomate.py`](mainapp/video_editting/creatomate.py): Video editing, merging, subtitle generation.
- [`mainapp/video_generation/Run_app.py`](mainapp/video_generation/Run_app.py): Orchestrates the full video generation pipeline.

## Notes

- The project uses SQLite by default; you can change the database URI
