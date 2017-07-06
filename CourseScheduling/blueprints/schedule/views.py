from flask import Blueprint, render_template

schedule = Blueprint('schedule', __name__, template_folder='templates')

@schedule.route('/schedule')
def schedule_output():
    return render_template('schedule/output.html')