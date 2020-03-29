from app import db
from models import Klass
from models.student import gen_auth, Student


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    enc_password = db.Column(db.String(128))
    auth_token = db.Column(db.String(128), default=gen_auth)

    def to_dict(self):
        d = dict(
            name=self.username,
            students=[s.to_dict(with_klass=False) for s in self.students],
        )

        return d

    @property
    def students(self):
        return db.session.query(Student).join(Klass).filter(Klass.teacher_id == self.id).all()
