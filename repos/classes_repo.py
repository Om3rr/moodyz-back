from sqlalchemy import desc
from sqlalchemy.orm import lazyload

from app import db
from datetime import datetime
from models import Vote, Klass, Student


class ClassesRepo(object):
    @classmethod
    def create_class(cls, class_name, teacher_id):
        klass = Klass(title=class_name, teacher_id=teacher_id)
        db.session.add(klass)
        db.session.commit()
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
        start_of_the_day = datetime.utcnow()
        start_of_the_day = start_of_the_day.replace(hour=0, minute=0, second=0)
        return start_of_the_day

    @classmethod
    def get_last_vote(cls, student_id):
        return db.session.query(Vote).filter(Vote.student_id == student_id).order_by(desc(Vote.pub_date)).first()

    @classmethod
    def get_by_slug(cls, slug):
        return db.session.query(Klass).filter(Klass.slug == slug).first()

    @classmethod
    def get_by_slug_and_teacher(cls, slug, teacher_id):
        return db.session.query(Klass).filter(Klass.slug == slug, Klass.teacher_id == teacher_id).first()

    @classmethod
    def get_klass_students(cls, klass_id):
        students = db.session.query(Student).filter(Student.klass_id == klass_id).all()
        return students

    @classmethod
    def get_votes(cls, klass_id, from_ts, to_ts):
        q = db.session.query(Vote).filter(Vote.klass_id == klass_id)
        if from_ts:
            q = q.filter(Vote.pub_date >= from_ts)
        if to_ts:
            q = q.filter(Vote.pub_date <= to_ts)
        return q.all()

    @classmethod
    def get_todays_response(cls, klass_id):
        students = cls.get_klass_students(klass_id)
        votes = cls.get_todays_votes(klass_id)
        res = []

        for student in students:
            selected_vote = None
            for vote in votes:
                if student.id == vote.student_id:
                    selected_vote = vote
                    break

            res.append(
                dict(
                    **student.to_dict(),
                    vote=getattr(selected_vote, 'to_dict', lambda: {})()
                )
            )
        return res

    @classmethod
    def get_todays_votes(cls, klass_id):
        votes = db.session.query(Vote).filter(Vote.klass_id == klass_id).filter(Vote.pub_date > cls.today()).all()
        return votes
