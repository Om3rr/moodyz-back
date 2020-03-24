from app import db
from models import Vote, Klass


class ClassesRepo(object):
    @classmethod
    def create_class(cls, class_name):
        klass =Klass(name=class_name)
        db.session.add(klass)
        return klass

    @classmethod
    def vote(cls, class_id, choice, name):
        v = Vote(klass_id=class_id, name=name, choice=choice)
        db.session.add(v)
        return v

    @classmethod
    def get_votes(cls, class_id):
        return db.session.query(Vote).filter(
            Vote.klass_id == class_id
        ).all()
