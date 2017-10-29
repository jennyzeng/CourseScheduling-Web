import os
from flask import flash, request, redirect, url_for
from flask_admin import BaseView, expose
from CourseScheduling.blueprints.admin.forms import FileUploadForm, CourseInfoUpdateForm
from database.Validator import InvalidJsonError
from database.loadHelper import load_course, load_requirement
from config.settings import UPLOAD_FOLDER
from CourseScheduling.blueprints.schedule.dbHelper import getQuarterCodes
# file upload in admin
# UPLOAD_FOLDER = '/CourseScheduling/database/txt_files/'


class FileUploadView(BaseView):
    UPLOAD_FOLDER = '/CourseScheduling/database/txt_files/'

    @expose('/', methods=['GET', 'POST'])
    def index(self):

        file_upload_form = FileUploadForm()
        update_form = CourseInfoUpdateForm()
        update_form.quarter_code.choices = getQuarterCodes()
        if file_upload_form.submit.data:
            if file_upload_form.validate_on_submit():
                self._handle_file_upload(file_upload_form)
            else:
                flash("Validation failed. Only JSON file is accepted.")
        elif update_form.download.data:
            if update_form.validate_on_submit():
                flash("download..")
        return self.render('admin/fileUpload.html', file_upload_form=file_upload_form, update_form = update_form)

    def _handle_file_upload(self, file_upload_form):
        file = file_upload_form.file.data
        flash(file.filename)
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        try:
            file_type = file_upload_form.fileType
            if file_type == "courses":
                load_course(path)
            elif file_type == "requirements":
                load_requirement(path)
        except (FileNotFoundError, InvalidJsonError, Warning) as e:
            flash("json loading ERROR: " + str(e))

        except Exception as e:
            flash("UNKOWN ERROR: " + str(e))
        else:
            flash("SUCCESS")
        finally:
            os.remove(path)

    def _handle_course_update(self, update_form):
        pass
