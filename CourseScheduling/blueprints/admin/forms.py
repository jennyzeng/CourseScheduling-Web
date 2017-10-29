from wtforms import form, fields, validators
from CourseScheduling.blueprints.user.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_uploads import UploadSet
from werkzeug.utils import secure_filename
from flask import request

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.objects(email=self.email.data).first()


class FileUploadForm(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(['json'])])
    fileType = fields.SelectField('File Type', choices=[('requirements', 'Requirements'), ('courses', 'Courses')])
    submit = fields.SubmitField('submit')

    def validate_on_submit(self):
        """
        Checks if form has been submitted and if so runs validate. This is
        a shortcut, equivalent to ``form.is_submitted() and form.validate()``
        """
        return self.is_submitted() and self.validate()

    def is_submitted(self):
        """
        Checks if form has been submitted. The default case is if the HTTP
        method is **POST**.
        """
        return request and request.method == "POST"


# class CourseInfoUpdateForm(FlaskForm):

