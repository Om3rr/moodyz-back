from app import db
from models import Student, Vote


class StudentRepo(object):
    @classmethod
    def get_student_by_auth(cls, auth_token):
        return db.session.query(Student).filter(Student.auth_token == auth_token).first()


    @classmethod
    def create_student(cls, name, picture, klass_id):
        student = Student(name=name, klass_id=klass_id)
        db.session.add(student)
        db.session.commit()
        return student
