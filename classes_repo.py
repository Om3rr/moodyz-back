from app import db
from datetime import datetime
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
    def get_todays_votes(cls, class_id):
        start_of_the_day = datetime.utcnow()
        start_of_the_day.replace(hour=0, minute=0, second=0)
        return db.session.query(Vote).filter(
            Vote.klass_id == class_id
        ).filter(Vote.pub_date > start_of_the_day).all()
