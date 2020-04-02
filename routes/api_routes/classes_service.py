from flask import Blueprint, jsonify, request, redirect, abort
from app import app
from authorizers import authorize_student, enhance_response_with_student_auth, authorize_student_or_teacher
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo

classes_service = Blueprint('/classes', __name__)


@classes_service.route('/me', methods=["GET"])
def show():
    student = authorize_student_or_teacher(request)
    klass_id = student.klass_id
    res = ClassesRepo.get_todays_response(klass_id)
    return jsonify({"students": res})


app.register_blueprint(classes_service, url_prefix="/api/classes")
