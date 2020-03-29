import random

from app import db
from models import Teacher, Klass, Student, Vote
from repos.teachers_repo import TeachersRepo

k = Klass(title="Test Class 1")
db.session.add(k)
db.session.commit()
t = TeachersRepo.create_teacher(username="omers", password="password")
k.teacher_id = k

names = """Teddie Manning
Teegan Mitchell
Chanel Coles
Robert Escobar
Allegra Hancock
Eben Thomas
Zayne Lamb
Liana Nelson
Sian Byrne
Rhiannon Storey""".split("\n")

ss = []
for name in names:
    s = Student(name=name, klass_id=1)
    db.session.add(s)
    ss.append(s)
db.session.commit()

for s in ss:
    v = Vote(student_id=s.id, klass_id=1, choice=random.choice([1, 2, 3]))
    db.session.add(v)

db.session.commit()
