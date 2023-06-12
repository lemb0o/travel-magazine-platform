from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from common.miscellaneous import get_file_path


# Create your models here.
class User(AbstractUser):
    """
user model that's Inheriting from AbstractUser which is a django Built-in
User model, it's very handy because it takes care of storing/hashing passwords
and Authenticating users.
    """
    username_validator = UnicodeUsernameValidator()  # support python3 only.

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits, periods and underscores only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=15)
    last_name = models.CharField(_('last name'), max_length=15)
    biography = models.TextField(_('biography'), null=True, blank=True, max_length=150)  # data isn't required
    avatar = models.ImageField(
        _('avatar'), default="avatars/no-avatar.jpg",
        # at every migration change get_file_path to "avatars/" to prevent a strange error!!.
        upload_to="avatars/"  # get_file_path(file_dir="avatars/"),
    )
    birth_date = models.DateField(_('birth date'), blank=True, null=True)

    NOT_SPECIFIED = 'N'
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (NOT_SPECIFIED, _('Not Specified')),
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=NOT_SPECIFIED)

    # the below is the required Authentication field by AbstractUser, its value is
    # the EmailField Cuz I choose it to force the user to authenticate using it.
    # the password is Handled Automatically by the module.
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    # the required fields obviously is the additional fields that will be
    # also stored with Email and password
    REQUIRED_FIELDS = ['birth_date', 'gender', 'email']

    def __str__(self):
        return self.username  # return the username as help text of each object.
