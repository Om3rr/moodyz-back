from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, redirect, abort
from app import app
from authorizers import authorize_student, enhance_response_with_student_auth, authorize_student_or_teacher, \
    authorize_teacher
from helpers.votes_helper import VotesHelper
from repos.classes_repo import ClassesRepo
from repos.students_repos import StudentRepo

classes_service = Blueprint('/classes', __name__)


@classes_service.route('/me', methods=["GET"])
def show():
    student = authorize_student(request)
    klass_id = student.klass_id
    res = ClassesRepo.get_todays_response(klass_id)
    return jsonify({"students": res})


@classes_service.route("/", methods=["POST"])
def create():
    klass = request.json.get("klass")
    teacher = authorize_teacher(request)
    klass = ClassesRepo.create_class(klass, teacher.id)
    return jsonify({
        "klass": klass.to_dict()
    })


@classes_service.route("/<klass_slug>/analytics", methods=["GET"])
def klass_analytics(klass_slug):
    teacher = authorize_teacher(request)
    klass = ClassesRepo.get_by_slug_and_teacher(klass_slug, teacher.id)
    students = klass.students
    from_ts, to_ts = request.args.get("from_ts"), request.args.get("to_ts")
    if from_ts:
        from_ts = datetime.fromtimestamp(int(from_ts))
    if to_ts:
        to_ts = datetime.fromtimestamp(int(to_ts))
    votes = ClassesRepo.get_votes(klass.id, from_ts, to_ts)
    dates_Array = VotesHelper.get_dates_array(from_ts, to_ts)
    result = VotesHelper.group_votes_by_student_and_enhance(votes, students, dates_Array)
    return jsonify(result)


app.register_blueprint(classes_service, url_prefix="/api/classes")
