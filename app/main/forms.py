from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name=StringField('What fuck your name !',validators=[Required()])
    submit=StringField('Fuck submit')
