from repos.students_repos import StudentRepo
from repos.teachers_repo import TeachersRepo


def authorize_student(request):
    student_auth = request.cookies.get("student")
    student = StudentRepo.get_student_by_auth(student_auth)
    if not student:
        raise Exception("Cant find student")
    return student


def enhance_response_with_student_auth(response, student):
    response.set_cookie("student", student.auth_token)


def authorize_teacher(request):
    teacher_auth = request.cookies.get("teacher")
    return TeachersRepo.find_teacher_by_auth(teacher_auth)
    # student = StudentRepo.get_student_by_auth(student_auth)


def enhance_response_with_teacher_auth(response, teacher):
    response.set_cookie("teacher", teacher.auth_token)
