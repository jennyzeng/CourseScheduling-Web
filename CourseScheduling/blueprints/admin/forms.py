from wtforms import form, fields


class reqForm(form.Form):
    name = fields.StringField('requirement name')


class MajorForm(form.Form):
    name = fields.StringField('Name')
    requirements = fields.FieldList(fields.FormField(reqForm))


class CourseForm(form.Form):
    dept = fields.StringField()
    cid = fields.StringField()
    name = fields.StringField()

    # guess it is better to change the prereq one later...
    # may change it to be a list of Courses not string.
    # so eventually we get a relational model = =...
    prereq = fields.FieldList(fields.FieldList(fields.StringField()))
    units = fields.FloatField()
    quarters = fields.FieldList(fields.DecimalField(min_value=0))
    upperOnly = fields.BooleanField(default=False)
    # for sample data in db right now, the pub_date is not correct
    # change the way we load data will fix this problem
    pub_date = fields.DateTimeField()