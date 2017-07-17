from CourseScheduling.blueprints.schedule.models import Course, Requirement
import lib.CourseSchedulingAlgorithm as cs
import warnings


def getCourse(dept, cid):
    c = Course.objects(dept=dept, cid=cid).first()
    return cs.Course(name=c.name, units=c.units, quarter_codes=c.quarters,
                     prereq=c.prereq, is_upper_only=c.upperOnly)


def getRequirements():
    return {r.name for r in Requirement.Objects()}


def getInfo(req):
    G, R, R_detail = dict(), dict(), dict()
    for r in req:
        R[r] = list()
        R_detail[r] = list()
        if Requirement.objects(name=r).first() == None:
            warnings.warn(r+"not exist")
            continue

        for subr in Requirement.objects(name=r).first().sub_reqs:
            c_set = set()
            R[r].append(subr.req_num)
            for c in subr.req_list:
                c_name = c.dept + " " + c.cid
                c_set.add(c_name)
                G[c_name] = cs.Course(name=c.name, units=c.units, quarter_codes=c.quarters,
                    prereq=c.prereq, is_upper_only=c.upperOnly)
            R_detail[r].append(c_set)
    return G, R, R_detail