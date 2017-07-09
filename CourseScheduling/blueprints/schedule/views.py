from flask import Blueprint, render_template
from CourseScheduling.blueprints.schedule.models import Course

schedule = Blueprint('schedule', __name__, template_folder='templates')
import logging

@schedule.route('/')
def schedule_home():
    return render_template('schedule/input.html')


@schedule.route('/test')
def test():
    output = []
    for course in Course.objects(dept='COMPSCI'):
        output.append(course.name)
    return str(output)


@schedule.route('/output')
def schedule_output():

    from lib.CourseSchedulingAlgorithm.Schedule import Schedule as CSschedule
    csschedule = CSschedule(widths={0: 13, 'else': 16})
    csschedule.L = [['I&CSCI31', 'MATH2A', 'I&CSCI6B', 'I&CSCI90'],
                  ['I&CSCI32', 'MATH2B', 'I&CSCI51'],
                  ['I&CSCI33', 'STATS67', 'I&CSCI6D', 'WRITINGLOW1'],
                  ['I&CSCI45C', 'I&CSCI6N', 'COMPSCI151', 'COMPSCI122A'],
                  ['I&CSCI46', 'COMPSCI178', 'GEII-1', 'GEII-2'],
                  ['COMPSCI132', 'COMPSCI177', 'HISTORY40C', 'POLSCI21A'],
                  ['COMPSCI161', 'COMPSCI171', 'HISTORY40A', 'IN4MATX43'],
                  ['COMPSCI116', 'COMPSCI164', 'COMPSCI112', 'COMPSCI175'],
                  ['COMPSCI165', 'I&CSCI53+53L', 'WRITINGLOW2'],
                  ['GEIII-1', 'GEIII-2', 'GEVI-1', 'GEVII-1'],
                  ['HISTORY40B', 'GEVIII-1', 'I&CSCI139W']]
    csschedule.curWidths = [13, 14, 16, 16, 16, 16, 16, 16, 14, 16, 12]
    max_row_length = max(len(row) for row in csschedule.L)
    return render_template('schedule/output.html',
                           schedule=csschedule, row_length=max_row_length)
