import datetime

from app import db
from helpers.random_gen import RandomGen
from models import Klass, Vote, Teacher
from repos.teachers_repo import TeachersRepo

t1 = TeachersRepo.create_teacher(username="מורה 4", password="ee8fe8ee8fe8ee8fe8")
k1 = Klass(title="Demo", teacher_id=t1.id)
db.session.add(k1)
db.session.commit()


def before_n_days(n=0):
    return datetime.datetime.utcnow() - datetime.timedelta(days=n)


for _ in range(10):
    student = RandomGen.get_student()
    student.klass_id = k1.id
    db.session.add(student)
    db.session.commit()
    for j in range(10):
        v = Vote(klass_id=k1.id, choice=RandomGen.get_choice(), student_id=student.id, pub_date=before_n_days(j))
        db.session.add(v)
    db.session.commit()

print("You can invite a teacher with the following url")
print("http://moodyzz.herokuapp.com/teachers/login?pw={}".format(t1.auth_token))
