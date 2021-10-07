from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, MultipleFileField, FloatField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from models import User
from flask_login import  current_user
from flask_wtf.file import FileField , FileAllowed



class RegisterForm(FlaskForm):
    fname = StringField(
        'First Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    lname = StringField(
        'Last Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField(
        'Sign Up'
    )

    def validate_username(self, fname):
        user = User.query.filter_by(fname=fname.data).first()
        if user:
            raise ValidationError("This name is already taken, Please choose a different one")

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This Email is already taken, Please choose a different one")        



class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField(
        'Log In'
    )

class UpdateAccountForm(FlaskForm):
    fname = StringField(
        'First Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    lname = StringField(
        'Last Name', validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'Email Address', validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    picture = FileField(
        'Update Display Image', validators=[FileAllowed(['png','jpg','jpeg'])]
    )
    submit = SubmitField(
        'Update'
    )

    def validate_username(self, fname):
        user = User.query.filter_by(fname=fname.data).first()
        if user:
            raise ValidationError("This name is already taken, Please choose a different one")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This Email is already taken, Please choose a different one")        


class SellersForm(FlaskForm):
    artist_name = StringField(
        'Artist Name', validators=[DataRequired()]
    )
    title = StringField(
        'Title', validators=[DataRequired()]
    )
    description = TextAreaField(
        'Description', validators=[DataRequired()]
    )
    category = SelectField(
        'Choose a Category', choices=[('Painting'),('Drawing/Sketch'),('Digital Art'), ('Handcrafts'), ('Other')]
    )
    image = FileField(
        'Upload Image', validators=[FileAllowed(['png','jpg','jpeg'])]
    )
    price = FloatField(
        'Price', validators=[DataRequired()]
    )
    quantity = IntegerField(
        'Quantity', validators=[DataRequired()]
    )
    submit = SubmitField(
        'Submit'
    )

class AddressForm(FlaskForm):
    address = TextAreaField(
        'Add Full Address', validators=[DataRequired()]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'Choose Your State', choices = [("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry")]
    )
    zip_code = IntegerField(
        'Zip-Code', validators=[DataRequired()]
    )
    submit = SubmitField(
        'Submit'
    )

class RequestResetForm(FlaskForm):
    email =  StringField(
        'Email', validators=[DataRequired(),Email(), Length(min=6,max=40)]
    )
    submit = SubmitField(
        'Request Reset Link'
    )
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account found with the email you entered!")        
   


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField(
        'Update Password'
    )