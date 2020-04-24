import itertools
from datetime import datetime, timedelta


class VotesHelper(object):
    @classmethod
    def group_votes_by_student_and_enhance(cls, votes, students, dates_array):
        res = []
        grouped_votes = itertools.groupby(votes, key=lambda vote: vote.student_id)
        for student_id, group in grouped_votes:
            students_votes = [vote.to_dict() for vote in group]
            s_date_array = [{}]*len(dates_array)
            for v in students_votes:
                key = dates_array.index(cls.get_date_by_timestamp(v.get("pub_date")))
                s_date_array[key] = v

            votes = itertools.groupby(students_votes, key=lambda vote: cls.get_date_by_timestamp(vote.get("pub_date")))
            votes = {k: [vv for vv in v] for k, v in votes}
            student = next(filter(lambda st: st.id == student_id, students))
            res.append(
                dict(
                    votes=votes, student=student.to_dict(), ordered_votes=s_date_array
                )
            )
        return res

    @classmethod
    def get_date_by_timestamp(cls, ts):
        return ts.strftime("%Y-%m-%d")

    @classmethod
    def get_dates_array(cls, from_ts, to_ts):
        print(from_ts, to_ts)
        currentTs = from_ts
        to_ts = datetime.strptime(to_ts.strftime("%Y-%m-%d"), "%Y-%m-%d") - timedelta(hours=1)
        dates = []
        dates.append(cls.get_date_by_timestamp(currentTs))
        while currentTs <= to_ts:
            currentTs += timedelta(days=1)
            dates.append(cls.get_date_by_timestamp(currentTs))
        print(dates)
        return dates
