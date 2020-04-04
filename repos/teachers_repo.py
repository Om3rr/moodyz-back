import hashlib

from app import db
from models import Teacher, Klass
import os


class TeachersRepo(object):
    @classmethod
    def find_teacher_by_username_password(cls, username, password):
        return db.session.query(Teacher).filter(Teacher.username == username).filter(
            Teacher.enc_password == cls.enc_password(password)).first()

    @classmethod
    def find_teacher_by_auth(cls, auth_token):
        return db.session.query(Teacher).filter(Teacher.auth_token == auth_token).first()

    @classmethod
    def create_teacher(cls, username, password):
        username_exist = db.session.query(Teacher.id).filter(Teacher.username == username).first()
        if username_exist:
            raise Exception("Username {} already exists".format(username))
        t = Teacher(
            username=username, enc_password=cls.enc_password(password)
        )
        db.session.add(t)
        db.session.commit()
        return t

    @staticmethod
    def enc_password(password):
        salt = os.getenv("PASSWORD_SALT")
        pepper = os.getenv("PASSWORD_PEPPER")
        better_pass = "{}{}{}".format(salt, password, pepper).encode("utf-8")
        return hashlib.sha256(better_pass).hexdigest()

    @staticmethod
    def get_class(teacher_id, klass_slug):
        klass = db.session.query(Klass).filter(Klass.teacher_id == teacher_id, Klass.slug == klass_slug).first()
        return klass
