from app import app
from flask import jsonify, request

from classes_repo import ClassesRepo


@app.route("/classes", methods=["POST"])
def create_class():
    content = request.json
    class_name = content.get("class_name")
    klass = ClassesRepo.create_class(class_name)
    return jsonify({"class": klass.to_dict()})


@app.route('/classes/<class_id>/today', methods=["GET"])
def classes_today(class_id):
    return jsonify({
        "votes": [vote.to_dict() for vote in ClassesRepo.get_votes(int(class_id))],
        "class_id": class_id
    })


@app.route("/classes/<class_id>/vote", methods=["POST"])
def vote(class_id):
    content = request.json
    voter_choice = content.get("choice")
    voter_name = content.get("name")
    ClassesRepo.vote(class_id, voter_choice, voter_name)
    return jsonify({"response": "OKAY :D"})


@app.route('/')
def hello_world():
    return 'Hello, World!2'
