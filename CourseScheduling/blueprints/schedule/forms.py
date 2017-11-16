from wtforms import form, fields, validators

class QuarterCreditForm(form.Form):
    quarterId = fields.SelectField(label="quarter id", validators=[validators.DataRequired()],
                                   choices=[(x,x) for x in range(15)], default=[(0,0)])
    credit = fields.SelectField(label="maximum credits allowed", validators=[validators.DataRequired()],
                                choices=[(x,x) for x in range(30)], default=[(16,16)])
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(QuarterCreditForm, self).__init__(csrf_enabled=False, *args, **kwargs)


class HomeInputForm(form.Form):
    majors =fields.SelectMultipleField(label="majors", validators=[validators.DataRequired()])
    firstQuarter = fields.SelectField(label="start quarter for scheduling", default=(0,0))
    quarterCreditDefault = fields.SelectField(label="default maximum credits per quarter" ,validators=[validators.DataRequired()],
                                choices=[(x,x) for x in range(30)], default=(16,16))
    quarterCredits = fields.FieldList(fields.FormField(QuarterCreditForm),
                                      label="maximum credits per quarter", validators=[validators.Optional()],
                                      min_entries=1, max_entries=15)
    next = fields.SubmitField('next')


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