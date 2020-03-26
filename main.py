from app import app
from flask import send_from_directory
from routes.api import api as api_service
import os


app.register_blueprint(api_service, url_prefix="/api")
# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # template_folder="build"
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    elif path != "" and os.path.exists(app.template_folder + "/" + path):
        return send_from_directory(app.template_folder, path)
    else:
        return send_from_directory(app.template_folder, 'index.html')





