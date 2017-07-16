from CourseScheduling.blueprints.schedule.models import Course, Requirement
import lib.CourseSchedulingAlgorithm as cs


def getCourse(dept, cid):
    c = Course.objects(dept=dept, cid=cid).first()
    return cs.Course(name=c.name, units=c.units, quarter_codes=c.quarters,
                     prereq=c.prereq, is_upper_only=c.upperOnly)


def getRequirements(reqs):
    R, R_detail = dict(), dict()
    for r in reqs:
        R[r] = list()
        R_detail[r] = list()
        for subr in Requirement.objects(name=r).first().sub_reqs:
            R[r].append(subr.req_num)
            R_detail[r].append(set(subr.req_list))
    return R, R_detail