import requests

from app import app
from flask import send_from_directory, jsonify, request, abort, redirect, make_response
from authorizers import enhance_response_with_student_auth, enhance_response_with_teacher_auth
from repos.students_repos import StudentRepo
from repos.teachers_repo import TeachersRepo
from routes.api import api as api_service
import os

app.register_blueprint(api_service, url_prefix="/api")

PROXY_HEADERS = [
    "Content-Type",
    "Date",
    "ETag",
    "Connection"
]


@app.route("/teachers/login", methods=["GET"])
def teacher_login():
    auth_token = request.args.get("pw")
    teacher = TeachersRepo.find_teacher_by_auth(auth_token)
    if not teacher:
        return abort(400)
    res = redirect("/")
    enhance_response_with_teacher_auth(res, teacher)
    return res


@app.route("/login", methods=["GET"])
def login():
    auth_token = request.args.get("pw")
    student = StudentRepo.get_student_by_auth(auth_token)
    if not student:
        return abort(400)
    res = redirect("/classes/new")
    enhance_response_with_student_auth(res, student)
    return res


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if "api/" in path:
        abort(404)
    fullpath = "{}/{}".format(os.getenv("WEBVIEW_URL"), path)
    res = requests.get(fullpath, headers=request.headers)
    resp = make_response(res.content)
    for key, value in res.headers.items():
        if key not in PROXY_HEADERS:
            continue
        resp.headers[key] = value
    return resp, res.status_code


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"response": "Not Found"}), 404


@app.errorhandler(400)
def page_not_found(error):
    return jsonify({"response": "Not Found"}), 404


@app.errorhandler(Exception)
def handle_exception(err):
    return jsonify({"error": str(err)}), 400
