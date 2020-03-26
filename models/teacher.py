from app import db


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klass_id = db.Column(db.Integer, db.ForeignKey('klass.id'),
                         nullable=False)
    name = db.Column(db.String(16))
    enc_password = db.Column(db.String(16))
    klass = db.relationship('Klass',
                            backref=db.backref('teachers', lazy=True))

    def to_dict(self):
        return dict(
            name=self.name,
            klass=self.klass.to_dict(),
        )
