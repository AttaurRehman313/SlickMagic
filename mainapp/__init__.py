from mainapp.model.database import db
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_PATH")
    app.json.sort_keys = False

    db.init_app(app)

    from mainapp.routes.video_link import link
    from mainapp.routes.image_generate import image
    from mainapp.routes.prompt import prompt
    from mainapp.routes.user_status import status
    

    app.register_blueprint(link, url_prefix="")
    app.register_blueprint(image,url_prefix="")
    app.register_blueprint(prompt, url_prefix="")
    app.register_blueprint(status, url_prefix="")
    

    return app

