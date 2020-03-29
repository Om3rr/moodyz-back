from flask import Blueprint, request, jsonify
from app import app
from authorizers import authorize_student, authorize_teacher, enhance_response_with_teacher_auth
from helpers.image_service import ProfilePicUploader
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo
from repos.teachers_repo import TeachersRepo

teachers_service = Blueprint('teachers', __name__)


@teachers_service.route('upload', methods=["POST"])
def upload_image():
    student = authorize_student(request)
    image = request.files.get("image")
    if not image:
        return jsonify({"Response": "Not found :("})
    result = ProfilePicUploader.upload(image)
    return jsonify({"Response": {
        "id": result.get("secure_url").split("/")[-1],
        "url": result.get("secure_url")
    }})


@teachers_service.route("login", methods=["POST"])
def login():
    body = request.json
    username, password = body.get("username"), body.get("password")
    teacher = TeachersRepo.find_teacher_by_username_password(username, password)
    response = jsonify({"teacher": teacher.to_dict()})
    enhance_response_with_teacher_auth(response, teacher)
    return response


@teachers_service.route("", methods=["POST"])
def create():
    username, password = request.json.get("username"), request.json.get("password")
    teacher = TeachersRepo.create_teacher(username, password)
    response = jsonify({"teacher": teacher.to_dict()})
    enhance_response_with_teacher_auth(response, teacher)
    return response


@teachers_service.route("/students", methods=["GET"])
def students():
    teacher = authorize_teacher(request)
    return jsonify({
        "students": [s.to_dict(with_klass=False) for s in teacher.students]
    })


@teachers_service.route("/students", methods=["POST"])
def create_student():
    body = request.json
    teacher = authorize_teacher(request)
    name, klass_slug, picture = body.get("name"), body.get("klass"), body.get("picture")
    klass = ClassesRepo.get_by_slug_and_teacher(klass_slug, teacher.id)
    if not klass:
        raise Exception("Can't find the relevant class")
    student = StudentRepo.create_student(name, picture, klass.id)
    return jsonify({"student": student.to_dict(with_klass=False)})


@teachers_service.route("/students", methods=["PUT"])
def edit_student():
    body = request.json
    name = body.get("name")
    picture = body.get("picture")
    student = StudentRepo.edit_student_picture_by_name(name, picture)
    return jsonify({"student": student.to_dict(with_klass=False)})


app.register_blueprint(teachers_service, url_prefix="/api/teachers")
