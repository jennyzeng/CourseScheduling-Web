from wtforms import form, fields, validators

class HomeInputForm(form.Form):
    majors =fields.SelectMultipleField(label="majors", validators=[validators.DataRequired()])
    firstQuarter = fields.SelectField(label="start quarter for scheduling", default='0')
    next = fields.SubmitField('next')
