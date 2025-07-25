from flask import send_from_directory
from flask import Blueprint
import os

link=Blueprint("link",__name__)

video_dir = os.getcwd()

@link.route("/video/<filename>")
def serve_video(filename):
    file_path = os.path.join(video_dir, filename)
    if not os.path.exists(file_path):
        return "Error: File not found", 404

    return send_from_directory(video_dir, filename)
