from flask_script import Command, Manager, Option
from CourseScheduling.app import create_app
from database import loadHelper
manager = Manager(create_app)


@manager.command
def load_course(filename="database/txt_files/fullcourses_new.txt"):
    loadHelper.load_course(filename)

@manager.command
def load_requirement(name='UNIVERSAL', filename='database/requirements/UNIVERSAL.json'):
    loadHelper.load_requirement(name, filename)


@manager.command
def hello(name='Yitong Wu'):
    print("hello", name)


if __name__ == "__main__":
    manager.run()
