import random
from datetime import date, datetime, timedelta

from app import db
from models import Teacher, Klass, Student, Vote
from repos.teachers_repo import TeachersRepo

k = Klass(title="Test Class 1")
db.session.add(k)
db.session.commit()
t = TeachersRepo.create_teacher(username="omerzzz", password="password")
k.teacher_id = t.id

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


pictures = """jrn8thz2tfxmchwahyr1.png
mle6mcgbuhq7ueofxgtf.png
hy4fqnlgmdcvdpx481up.png
kmsrmi26hix2vm3t0hem.png
a0iumvhijg90vigzqzyq.png
mug41ae0g93lm8ad0vnh.png
tldkubag7qnp6gipgfja.png
r8uzgjwa66rfyug1ljf0.png
cipyycnlc1xdgkav2h8j.png
jrn8thz2tfxmchwahyr1.png
igehqh8wu3wf4leqikky.png
igehqh8wu3wf4leqikky.png
igehqh8wu3wf4leqikky.png
igehqh8wu3wf4leqikky.png
igehqh8wu3wf4leqikky.png
fi9usl0rq5iqopiayxni.png
g9ubzqyroptg0kbuz3sr.png
jsktubd7pfaa1lf9g2ho.png
hnjdzkt0zdnbf690ubkf.png
s8ynxlmtnewxuwoc45vc.png
loqpgsraopuxaax6kvhu.png
s1x6pwl1bvlw8pki8wrh.png
b92nad0dwpeycvqxvrhl.png
znztmyjqlmvqqknbaced.png
z6ps1drnswnjndsf3lvu.png
sgqn8m7fzptjy07xtbrs.png
j1y4ulsr0qiqhuopn0pb.png
oadm6fjdul81nm4mdyti.png
cjk72cu2llth2xpag75n.png
tzvvtnix8bsivvi0kbxw.png""".split("\n")

genders = ["male", "female"]

ss = []
for i in range(10):
    name = random.choice(names)
    picture_url = random.choice(pictures)
    gender = random.choice(genders)
    s = Student(name=name, picture_url=picture_url, gender=gender, klass_id=k.id)
    db.session.add(s)
    ss.append(s)
db.session.commit()

for s in ss:
    for i in range(10):
        pubdate = datetime.utcnow() - timedelta(days=i)
        v = Vote(student_id=s.id, klass_id=k.id, pub_date=pubdate, choice=random.choice([1, 2, 3, 4,5]))
        db.session.add(v)

db.session.commit()
