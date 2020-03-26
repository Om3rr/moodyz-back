from sqlalchemy.orm import lazyload

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
    def vote(cls, student_id, class_id, choice):
        v = Vote(klass_id=class_id, choice=choice, student_id=student_id)
        db.session.add(v)
        db.session.commit()
        return v

    @classmethod
    def edit_or_create_vote(cls, student_id, klass_id, choice):
        vote = cls.get_last_vote(student_id)
        if vote and (vote.pub_date > cls.today()):
            vote.choice = choice
            db.session.commit()
            return vote
        else:
            return cls.vote(student_id, klass_id, choice)

    @classmethod
    def today(cls):
        today = datetime.utcnow().date()
        start = datetime(today.year, today.month, today.day)
        return start

    @classmethod
    def get_last_vote(cls, student_id):
        return db.session.query(Vote).filter(Vote.student_id == student_id).order_by(Vote.pub_date).first()

    @classmethod
    def get_todays_votes(cls, class_id):
        start_of_the_day = datetime.utcnow()
        start_of_the_day = start_of_the_day.replace(hour=0, minute=0, second=0)
        return db.session.query(Vote).options(lazyload('student')).filter(
            Vote.klass_id == class_id
        ).filter(Vote.pub_date > start_of_the_day).all()

    @classmethod
    def get_by_slug(cls, slug):
        return db.session.query(Klass).filter(Klass.slug == slug).first()
