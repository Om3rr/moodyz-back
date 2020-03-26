from app import db
from datetime import datetime


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klass_id = db.Column(db.Integer, db.ForeignKey('klass.id'),
                         nullable=False)
    name = db.Column(db.String(16))
    choice = db.Column(db.Integer)
    klass = db.relationship('Klass',
                            backref=db.backref('votes', lazy=True))
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)

    def to_dict(self):
        return dict(
            name=self.name,
            choice=self.choice,
            pub_date=self.pub_date
        )
