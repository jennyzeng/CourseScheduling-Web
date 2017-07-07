from flask import Blueprint, render_template

schedule = Blueprint('schedule', __name__, template_folder='templates')
import logging
@schedule.route('/schedule')
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

#
# layer: 0, with width 13 and max 13
# I&CSCI31; MATH2A; I&CSCI6B; I&CSCI90
#
# layer: 1, with width 14 and max 16
# I&CSCI32; MATH2B; I&CSCI51
#
# layer: 2, with width 16 and max 16
# I&CSCI33; STATS67; I&CSCI6D; WRITINGLOW1
#
# layer: 3, with width 16 and max 16
# I&CSCI45C; I&CSCI6N; COMPSCI151; COMPSCI122A
#
# layer: 4, with width 16 and max 16
# I&CSCI46; COMPSCI178; GEII-1; GEII-2
#
# layer: 5, with width 16 and max 16
# COMPSCI132; COMPSCI177; HISTORY40C; POLSCI21A
#
# layer: 6, with width 16 and max 16
# COMPSCI161; COMPSCI171; HISTORY40A; IN4MATX43
#
# layer: 7, with width 16 and max 16
# COMPSCI116; COMPSCI164; COMPSCI112; COMPSCI175
#
# layer: 8, with width 14 and max 16
# COMPSCI165; I&CSCI53+53L; WRITINGLOW2
#
# layer: 9, with width 16 and max 16
# GEIII-1; GEIII-2; GEVI-1; GEVII-1
#
# layer: 10, with width 12 and max 16
# HISTORY40B; GEVIII-1; I&CSCI139W