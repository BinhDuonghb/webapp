from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,EmailField,TextAreaField,FloatField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError
from coffe.model import User
class RegisterFrom(FlaskForm):
    def validate_username(self, username_to_check):
        username = User.query.filter_by(name=username_to_check.data).first()
        if  username:
            raise ValidationError("This username is already been used")
    def validate_email(self,email_to_check):
        email =User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise  ValidationError('The Email has already been registered')
    username = StringField(label="User name",validators=[Length(min=2,max=10),DataRequired()])
    email = EmailField(label="Email",validators=[Email(),DataRequired()])
    password1 = PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm password",validators=[EqualTo('password1'),DataRequired()])
    submit= SubmitField("Register")

class LoginForm(FlaskForm):
    userName = StringField(label="User Name",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField("Login")
class PurchaseItem(FlaskForm):
    submit =SubmitField("Purchase")
class UploadImageForm(FlaskForm):
    submit =SubmitField("Submit Change")

class AddItemForm(FlaskForm):
    itemName = StringField("Item Name", validators=[DataRequired()])
    price = FloatField("Item Price", validators=[DataRequired()])
    description = TextAreaField("Item Description (more than 15 words)", validators=[DataRequired(),Length(min=15)])
    submit = SubmitField("Add Item")
    
class DepositForm(FlaskForm):
    cash = FloatField(validators=[DataRequired()])
    submit = SubmitField("Cash in")