from repos.students_repos import StudentRepo


def authorize_student(request):
    student_auth = request.cookies.get("student")
    student = StudentRepo.get_student_by_auth(student_auth)
    if not student:
        raise Exception("Cant find student")
    return student


def authorize_teacher(request):
    teacher_auth = request.cookies.get("student")
    # student = StudentRepo.get_student_by_auth(student_auth)
