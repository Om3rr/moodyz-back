from app import app
from flask import jsonify, request, Blueprint, send_from_directory
import os
from classes_repo import ClassesRepo

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



api = Blueprint('api', __name__)
@api.route("/classes", methods=["POST"])
def create_class():
    content = request.json
    class_name = content.get("class_name")
    klass = ClassesRepo.create_class(class_name)
    return jsonify({"class": klass.to_dict()})


@api.route('/classes/<class_id>/today', methods=["GET"])
def classes_today(class_id):
    return jsonify({
        "votes": [vote.to_dict() for vote in ClassesRepo.get_todays_votes(int(class_id))],
        "class_id": class_id
    })


@api.route("/classes/<class_id>/vote", methods=["POST"])
def vote(class_id):
    content = request.json
    voter_choice = content.get("choice")
    voter_name = content.get("name")
    ClassesRepo.vote(class_id, voter_choice, voter_name)
    return jsonify({"response": "OKAY :D"})

