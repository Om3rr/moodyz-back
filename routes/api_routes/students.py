from flask import Blueprint, jsonify, request, redirect
from app import app
from authorizers import authorize_student
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo

student_service = Blueprint('/students', __name__)


@student_service.route("/login", methods=["GET"])
def student_login():
    auth_token = request.args.get("pw")
    student = StudentRepo.get_student_by_auth(auth_token)
    if not student:
        return jsonify({"error": "Not Found"}, 400)
    res = redirect(student.klass.url)
    res.set_cookie("student", student.auth_token)
    return res


@student_service.route("/", methods=["POST"])
def create_student():
    content = request.json
    klass_slug = content.get("klass")
    klass = ClassesRepo.get_by_slug(klass_slug)
    name = content.get("name")
    student = StudentRepo.create_student(name, "", klass.id)
    return jsonify({"student": student.to_dict()})


@student_service.route("/me", methods=["GET"])
def me():
    student = authorize_student(request)
    return jsonify({"student": student.to_dict()})


@student_service.route("/vote", methods=["POST"])
def vote():
    student = authorize_student(request)
    klass = student.klass
    body = request.json
    choice = body.get("choice")
    ClassesRepo.edit_or_create_vote(student.id, klass.id, choice)
    votes = ClassesRepo.get_todays_votes(klass.id)
    return jsonify({"votes": [v.to_dict() for v in votes]})


app.register_blueprint(student_service, url_prefix="/api/students")
