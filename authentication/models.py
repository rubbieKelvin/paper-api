from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
	"""a custom user model
	"""

	username = None
	email = models.EmailField(verbose_name=_('email address'), unique=True, max_length=100)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email