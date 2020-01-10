from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


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
