import random

from models import Student

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


class RandomGen(object):
    @classmethod
    def get_name(cls):
        return random.choice(names)

    @classmethod
    def get_picture(cls):
        return random.choice(pictures)

    @classmethod
    def get_gender(cls):
        return random.choice(genders)

    @classmethod
    def get_choice(cls):
        return random.choice([0, 200, 300, 400, 500, 600, 700, 800, 900])

    @classmethod
    def get_student(cls):
        return Student(name=cls.get_name(), gender=cls.get_gender(), picture_url=cls.get_picture())
