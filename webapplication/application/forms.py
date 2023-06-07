from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField , SelectField , IntegerField , StringField , PasswordField  , DateField
from wtforms.validators import Length, InputRequired, ValidationError,NumberRange , Email  , EqualTo , Length , Optional
def length_validator(form, field):#from wtforms.fields.html5 import DateField

    l = field.data
    print(field.data)
    if l == '':
        raise ValidationError("No Value Chosen")
    
    
class LoginForm(FlaskForm):
    username = StringField('Username (Username) \n Email must be a username' , validators = [InputRequired() , Email()])
    password = PasswordField("Password" , validators= [InputRequired()] )
    submit = SubmitField("Login")
    
class SignUpForm(FlaskForm):
    username = StringField('Username' , validators = [InputRequired() , Email()  ])
    password = PasswordField("Password" , validators= [InputRequired()] )
    confirmpassword = PasswordField("Password  Confirm" , validators= [InputRequired()  , EqualTo('password')] )
    submit = SubmitField("Sign Up")

    
    
    
class FilterSearchForm(FlaskForm):
    mindate = DateField('Start Date' , validators = [Optional()])
    maxdate = DateField('End Date', validators = [Optional()])
    model = SelectField('Model', choices=[('both','both') , ('vgg', 'Visual Geometry Group'),('wideresnet', 'Wide ResNet')], validators = [InputRequired() , length_validator])
    submit = SubmitField("Search and Filter")
    