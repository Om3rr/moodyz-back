from app import db
import string
import random


def gen_slug():
    return "".join([random.choice(string.ascii_letters) for i in range(10)])


class Klass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16))
    slug = db.Column(db.String(16), index=True, default=gen_slug)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher',
                              backref=db.backref('klasses', lazy=True))

    @property
    def url(self):
        return "/classes/{}".format(self.slug)

    def to_dict(self):
        return dict(title=self.title, url=self.url, slug=self.slug)
