from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Checkbook (models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20, validators=[MinLengthValidator(3, "length of characters is too small")])
	starred = models.BooleanField(default=False)

	date_created = models.DateTimeField(auto_now_add=True)
	date_edited  = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.name
	

# checkbook membership
class CheckbookMembership (models.Model):
	ROLE = (
		("ON", "OWNER"),
		("OB", "OBSERVER"),
		("ED", "EDITOR")
	)

	user = models.ForeignKey("authentication.User", related_name="checkbook_memberships", on_delete=models.CASCADE)
	checkbook = models.ForeignKey("Checkbook", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	role = models.TextField(max_length=2, choices=ROLE)
