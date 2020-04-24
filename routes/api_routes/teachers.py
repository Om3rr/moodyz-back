from flask import Blueprint, request, jsonify, abort
from app import app, db
from authorizers import authorize_student, authorize_teacher, enhance_response_with_teacher_auth, \
    authorize_student_or_teacher
from helpers.image_service import ProfilePicUploader
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo
from repos.teachers_repo import TeachersRepo

teachers_service = Blueprint('teachers', __name__)


@teachers_service.route('upload', methods=["POST"])
def upload_image():
    authorize_student_or_teacher(request)
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


@teachers_service.route("/classes/<class_slug>", methods=["GET"])
def students(class_slug):
    teacher = authorize_teacher(request)
    klass = TeachersRepo.get_class(teacher.id, class_slug)
    return jsonify({
        "students": [s.to_dict() for s in klass.students],
        "klass": klass.to_dict()
    })


@teachers_service.route("/classes/<class_slug>/students", methods=["POST"])
def create_student(class_slug):
    student = request.json.get("student")
    teacher = authorize_teacher(request)
    name, picture, gender = student.get("name"), student.get("pictureId"), student.get("gender")
    klass = ClassesRepo.get_by_slug_and_teacher(class_slug, teacher.id)
    if not klass:
        raise Exception("Can't find the relevant class")
    student = StudentRepo.create_student(name, picture, gender, klass.id)
    return jsonify({"student": student.to_dict(with_klass=False)})


@teachers_service.route("/classes/<class_id>/students/<student_id>", methods=["PUT"])
def edit_student(class_id, student_id):
    teacher = authorize_teacher(request)
    body = request.json
    name = body.get("name")
    picture = body.get("picture")
    student = StudentRepo.get_student_by_teacher(teacher.id, student_id)
    if not student:
        return abort(404)
    student = StudentRepo.edit_student_picture_by_name(student_id, name, picture)
    return jsonify({"student": student.to_dict(with_klass=False)})


@teachers_service.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    teacher = authorize_teacher(request)
    student = StudentRepo.get_student_by_teacher(teacher.id, student_id)
    if not student:
        return abort(404)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"okay": True})


@teachers_service.route("/me", methods=["GET"])
def me():
    teacher = authorize_teacher(request)
    print(teacher)
    return jsonify({
        "teacher": teacher.to_dict(),
        "klasses": [klass.to_dict() for klass in teacher.klasses]
    })


app.register_blueprint(teachers_service, url_prefix="/api/teachers")
