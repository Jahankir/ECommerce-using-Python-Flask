from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from eCommerce import db

# class StockImport(FlaskForm):

#     def validate_barcode(self, barcode_to_check):
#         barcode = db.item.find_one({'barcode': barcode_to_check.data})
#         if barcode:
#             raise ValidationError ('barcode already exist! please try another barcode.')

#     name = StringField('Name', validators=[DataRequired(), Length(max=50)])
#     barcode = StringField('Barcode', validators=[DataRequired(), Length(min=12,max=12)])
#     price = IntegerField('Price', validators=[DataRequired()])
#     description = StringField('Description', validators=[DataRequired(), Length(max=1024)])
#     imageUrl = StringField('Image Url', validators=[DataRequired()])
#     submit = SubmitField('Add Product')

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        username = db.user.find_one({'username': username_to_check.data})
        if username:
            raise ValidationError ('Username Already exist! please try another username.')
        
    def validate_email(self, email_to_check):
        email = db.user.find_one({'email': email_to_check.data})
        if email:
            raise ValidationError ('Email already exist! please try another email.')

    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')