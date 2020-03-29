from app import app
from flask import send_from_directory, jsonify, request, abort, redirect

from authorizers import enhance_response_with_student_auth
from repos.students_repos import StudentRepo
from routes.api import api as api_service
import os

app.register_blueprint(api_service, url_prefix="/api")


@app.route("/login", methods=["GET"])
def login():
    auth_token = request.args.get("pw")
    student = StudentRepo.get_student_by_auth(auth_token)
    if not student:
        return abort(400)
    res = redirect(student.klass.url)
    enhance_response_with_student_auth(res, student)
    return redirect("http://localhost:3000/classes/{}".format(student.klass_id))

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    elif path != "" and os.path.exists(app.template_folder + "/" + path):
        return send_from_directory(app.template_folder, path)
    else:
        return send_from_directory(app.template_folder, 'index.html')

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"response": "Not Found"}), 404


@app.errorhandler(400)
def page_not_found(error):
    return jsonify({"response": "Not Found"}), 404


@app.errorhandler(Exception)
def handle_exception(err):
    return jsonify({"error": str(err)}), 400
