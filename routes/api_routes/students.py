from flask import Blueprint, jsonify, request, redirect, abort
from app import app
from authorizers import authorize_student, enhance_response_with_student_auth, authorize_teacher
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo

student_service = Blueprint('/students', __name__)


@student_service.route("/login", methods=["GET"])
def student_login():
    auth_token = request.args.get("pw")
    student = StudentRepo.get_student_by_auth(auth_token)
    if not student:
        return abort(400)
    res = redirect(student.klass.url)
    enhance_response_with_student_auth(res, student)
    return res


@student_service.route("/", methods=["POST"])
def create_student():
    teacher = authorize_teacher(request)
    student_json = request.json.get("student")
    name = student_json.get("name")
    picture_id = student_json.get("pictureId")
    student = StudentRepo.create_student(name, picture_id, teacher.klasses[0].id)
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
    res = ClassesRepo.get_todays_response(klass.id)
    return jsonify({"students": res})


app.register_blueprint(student_service, url_prefix="/api/students")
