from flask import Blueprint, request, jsonify

from authorizers import authorize_student, enhance_response_with_teacher_auth
from repos.classes_repo import ClassesRepo
from repos.teachers_repo import TeachersRepo
from routes.api_routes.students import student_service
from routes.api_routes.teachers import teachers_service
import routes.api_routes.classes_service

api = Blueprint('/api', __name__)


@api.route("/classes", methods=["POST"])
def create_class():
    content = request.json
    class_name = content.get("class_name")
    klass = ClassesRepo.create_class(class_name)
    return jsonify({"class": klass.to_dict()})


@api.route('/classes/today', methods=["GET"])
def classes_today():
    student = authorize_student(request)
    students = ClassesRepo.get_students_with_last_votes(student.klass.id)

    return jsonify({
        "votes": [vote.to_dict() for vote in students],
    })


@api.route("/classes/<class_id>/vote", methods=["POST"])
def vote(class_id):
    content = request.json
    voter_choice = content.get("choice")
    voter_name = content.get("name")
    ClassesRepo.vote(class_id, voter_choice, voter_name)
    return jsonify({"response": "OKAY :D"})


@api.route("/login", methods=["POST"])
def login():
    content = request.json
    username = content.get("username")
    password = content.get("password")
    teacher = TeachersRepo.find_teacher_by_username_password(username, password)
    if not teacher:
        return jsonify("Not found"), 404
    response = jsonify({"teacher": teacher.to_dict()})
    enhance_response_with_teacher_auth(response, teacher)
    return response
