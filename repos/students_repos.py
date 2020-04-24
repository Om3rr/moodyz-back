from app import db
from models import Student, Vote, Klass


class StudentRepo(object):
    @classmethod
    def get_student_by_auth(cls, auth_token):
        return db.session.query(Student).filter(Student.auth_token == auth_token).first()

    @classmethod
    def create_student(cls, name, picture, gender, klass_id):
        s = db.session.query(Student).filter(Student.name == name).filter(Student.klass_id==klass_id).first()
        if s:
            raise Exception("Student name already exists")
        student = Student(name=name, gender=gender, klass_id=klass_id, picture_url=picture)
        db.session.add(student)
        db.session.commit()
        return student

    @classmethod
    def edit_student_picture_by_name(cls, student_id, name, picture_url):
        student = db.session.query(Student).filter(Student.id == student_id).first()
        student.picture_url = picture_url
        student.name = name
        db.session.commit()
        return db.session.query(Student).filter(Student.id == student_id).first()

    @classmethod
    def get_student_by_teacher(cls, teacher_id, student_id):
        return db.session.query(Student).join(Klass).filter(Klass.teacher_id == teacher_id,
                                                            Student.id == student_id).first()
