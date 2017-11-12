from CourseScheduling.blueprints.schedule.models import Course, Requirement, Major, Quarter
import lib.CourseSchedulingAlgorithm as cs
import warnings
import logging

def getCourse(dept, cid):
    c = Course.objects(dept=dept, cid=cid).first()
    return cs.Course(name=c.name, units=c.units, quarter_codes=c.quarters,
                     prereq=c.prereq, is_upper_only=c.upperOnly)


def getMajorsNames():
    """
    :return:  list of major names
    """
    return [m.name for m in Major.objects()]

def getMajorModel():
    """
    :return: all majors with their information defined in models.py
    """
    return list(Major.objects())


def getMajorReqNspecs(major):
    """
    :param major: should be the model defined in models.py
    :return:
    """
    if major:
        return major.requirements, major.specs
    return [], []

def getMajorReqNspecsByName(major_name):
    """
    :param major_name: name of the major
    :return: a list of major requirements, and a list of major sepcs
    """
    m = Major.objects(name=major_name)
    if m.first():
        return m.first().requirements, m.first().specs
    return [],[]


def getMajorRequirementsByName(major_name):
    """
    :param major_name: name of the major
    :return: a list of major requirements, (requirement is defined in models.py)
    """
    m = Major.objects(name=major_name)
    if m.first():
        return m.first().requirements
    return []

def getMajorSpecsByName(major_name):
    """
    :param major_name: name of the major
    :return: a list of major specs, (spec is also a requirement defined in models.py)
    """
    m = Major.objects(name=major_name)
    if m.first():
        return m.first().specs
    return []

def getQuarterCodes():
    """
    :return:
    """
    quarters = Quarter.objects()
    return [(q.code, q.name) for q in quarters]

def getInfo(req):
    G, R, R_detail = dict(), dict(), dict()
    for r in req:
        R[r] = list()
        R_detail[r] = list()
        if Requirement.objects(name=r).first() == None:
            warnings.warn(r + "not exist")
            continue

        for subr in Requirement.objects(name=r).first().sub_reqs:
            c_set = set()
            R[r].append(subr.req_num)
            for c in subr.req_list:
                c_name = c.dept + " " + c.cid
                c_set.add(c_name)
                G[c_name] = cs.Course(name=c.name, units=c.units,
                                      quarter_codes=convert_quarters(c.quarters),
                                      prereq=convert_prereq(c.prereq),
                                      is_upper_only=c.upperOnly,
                                      priority=c.priority)
            R_detail[r].append(c_set)
    return G, R, R_detail


def convert_prereq(prereq):
    output = []
    for or_set in prereq:
        output.append([])
        for course in or_set:
            output[-1].append(course.dept + " " + course.cid)
    return output


def convert_quarters(quarters):
    for idx, q in enumerate(quarters):
        quarters[idx] = q.code
    return quarters
