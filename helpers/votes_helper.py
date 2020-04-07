import itertools
from datetime import datetime


class VotesHelper(object):
    @classmethod
    def group_votes_by_student_and_enhance(cls, votes, students):
        res = []
        grouped_votes = itertools.groupby(votes, key=lambda vote: vote.student_id)
        for student_id, group in grouped_votes:
            students_votes = [vote.to_dict() for vote in group]
            votes = itertools.groupby(students_votes, key=lambda vote: cls.get_date_by_timestamp(vote.get("pub_date")))
            votes = {k: [vv for vv in v] for k, v in votes}
            student = next(filter(lambda st: st.id == student_id, students))
            res.append(
                dict(
                    votes=votes, student=student.to_dict()
                )
            )
        return res

    @classmethod
    def get_date_by_timestamp(cls, ts):
        return ts.strftime("%Y-%m-%d")
