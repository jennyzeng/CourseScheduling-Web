from flask_security import current_user
from flask import Blueprint, render_template, url_for, redirect, request
from CourseScheduling.blueprints.user.forms import LoginForm
users = Blueprint('users', __name__, template_folder='templates')
from flask_login import login_user, logout_user


@users.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('user/form.html', form=form)


@users.route('/logout/')
def logout_view():
    logout_user()
    return redirect(url_for('schedule.schedule_home'))

