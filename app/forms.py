from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class SheetForm(FlaskForm):
    character_name = StringField('Character Name')
    level = IntegerField('Level', validators=[DataRequired()])
    race = StringField('Race/Species')
    job = SelectField('Classes', choices=[('Barbarian', 'Barbarian'), ('Fighter', 'Fighter'), ('Paladin', 'Paladin'), ('Bard', 'Bard'), ('Sorcerer', 'Sorcerer'), (
        'Warlock', 'Warlock'), ('Cleric', 'Cleric'), ('Druid', 'Druid'), ('Monk', 'Monk'), ('Ranger', 'Ranger'), ('Rogue', 'Rogue'), ('Wizard', 'Wizard')])
    body = TextAreaField('Character Description',
                         validators=[Length(min=0, max=250)])
    submit = SubmitField('Submit')


class EditSheetForm(FlaskForm):
    character_name = StringField('Character Name')
    level = IntegerField('Level', validators=[DataRequired()])
    race = StringField('Race/Species')
    job = SelectField('Classes', choices=[('Barbarian', 'Barbarian'), ('Fighter', 'Fighter'), ('Paladin', 'Paladin'), ('Bard', 'Bard'), ('Sorcerer', 'Sorcerer'), (
        'Warlock', 'Warlock'), ('Cleric', 'Cleric'), ('Druid', 'Druid'), ('Monk', 'Monk'), ('Ranger', 'Ranger'), ('Rogue', 'Rogue'), ('Wizard', 'Wizard')])
    body = TextAreaField('Character Description',
                         validators=[Length(min=0, max=250)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
            super(EditSheetForm, self).__init__(*args, **kwargs)


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
