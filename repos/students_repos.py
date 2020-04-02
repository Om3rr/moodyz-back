from app import db
from models import Student, Vote


class StudentRepo(object):
    @classmethod
    def get_student_by_auth(cls, auth_token):
        return db.session.query(Student).filter(Student.auth_token == auth_token).first()


    @classmethod
    def create_student(cls, name, picture, klass_id):
        s = db.session.query(Student).filter(Student.name == name).first()
        if s:
            raise Exception("Student name already exists")
        student = Student(name=name, klass_id=klass_id, picture_url=picture)
        db.session.add(student)
        db.session.commit()
        return student

    @classmethod
    def edit_student_picture_by_name(cls, name, picture):
        db.session.query(Student).filter(Student.name == name).update(picture)
        db.session.commit()
        return db.session.query(Student).filter(Student.name == name).first()
