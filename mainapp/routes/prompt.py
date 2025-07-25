from flask import Blueprint, request
from mainapp.model.scripts_generation import create_script


prompt=Blueprint("prompt",__name__)
@prompt.route("/prompt", methods=["POST"])
def make_prompt():
    try:
        text = request.json["text"]
        number = request.json["number"]
    except Exception as e:
        return f"Error while handling input : {e}"

    script = create_script(text, number)
    return script
