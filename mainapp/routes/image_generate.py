from mainapp.video_editting.font_and_effect import video_aspect_ratio,select_aspect_ratio
from mainapp.multi_users_process.queue_process import request_queue
from mainapp.model.database import User,db
from flask import blueprints,request,jsonify
from datetime import datetime
import threading

image = blueprints.Blueprint("generate",__name__)

@image.route("/generate",methods=["POST"])
def generate():
    try:
        user_id = request.json["user_id"]
        video_id = request.json["video_id"]
        script = request.json["script"]
        setting = request.json["setting"]
        aspect_ratio = request.json["aspect_ratio"]
        # voice = request.json["voice"]
        get_theme = request.json["theme"]

        if not get_theme:
            theme = "realistic"
        else:
            theme = get_theme
    except Exception as e:
        return f"Error while handling input : {e}"

    height, width = video_aspect_ratio(value=aspect_ratio)
    selected_ratio = select_aspect_ratio(value=aspect_ratio)

    if setting.lower() == "default":
        font_family = "Montserrat"
        font_size = "9.00 vmin"
        # voice = random.choice(list(voices.values()))
        transcript_effect = "bounce"
        stroke_color = "#000000"
        font_weight = "800"
        fill_color = "white"
        max_length = 1

    elif setting.lower() == "manual":
        font_family = request.json["font_family"]
        font_float = float(request.json["font_size"])
        font_size = str(font_float) + " vmin"
        # voice = request.json["voice"]
        # voice = voices[voice]
        transcript_effect = request.json["transcript_effect"]
        stroke_color = request.json["stroke_color"]
        font_weight = request.json["font_weight"]
        fill_color = request.json["fill_color"]
        max_length = request.json["max_length"]

    # Check if the user and video combination already exists
    old_user = User.query.filter_by(user_id=user_id, video_id=video_id).first()
    count = f"{user_id}_{video_id}"
    if not user_id or not video_id:
        return "Error! User ID or Video ID missing", 400

    if not old_user:
        request_id = f"{user_id}_{datetime.now().timestamp()}"
        with threading.Lock():  # Avoid duplicate requests
            if any(req["request_id"] == request_id for req in request_queue):
                return jsonify({"message": "Request is already queued."}), 400

            user_request = {
                "request_id": request_id,
                "params": {
                    "script": script,
                    "aspect_ratio": selected_ratio,
                    "font_family": font_family,
                    "font_size": font_size,
                    "transcript_effect": transcript_effect,
                    "stroke_color": stroke_color,
                    "font_weight": font_weight,
                    "fill_color": fill_color,
                    "max_length": max_length,
                    "height": height,
                    "width": width,
                    "theme": theme,
                    "count": count,
                },
            }
            request_queue.append(user_request)

        # Add new user and video record to the database
        try:
            user = User(user_id=user_id, video_id=video_id, count=count, script=script)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return f"Database error: {e}", 500

        return jsonify(
            {
                "request_id": request_id,
                "message": "Your request has been queued. Check status later.",
            }
        )
    else:
        return "Error! This User and Video combination already exist.", 400
