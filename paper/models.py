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


# saves text contents in check books
class TextItem (models.Model):
	id = models.AutoField(primary_key=True)
	checkbook = models.ForeignKey("Checkbook", related_name="texts", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	last_edited = models.DateTimeField(auto_now=True)
	text = models.TextField(verbose_name="value")
	title = models.CharField(max_length=20, null=False, blank=False)


# saves image files in check books
class ImageItem (models.Model):
	id = models.AutoField(primary_key=True)
	checkbook = models.ForeignKey("Checkbook", related_name="images", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	last_edited = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to="uploads/images/")
	title = models.CharField(max_length=20, null=False, blank=False)

# saves audio files in checkbooks
# this will need futher manual-validation
class AudioItem (models.Model) :
	id = models.AutoField(primary_key=True)
	checkbook = models.ForeignKey("Checkbook", related_name="voicenotes", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	last_edited = models.DateTimeField(auto_now=True)
	audio = models.FileField(upload_to="uploads/notes/")
	title = models.CharField(max_length=20, null=False, blank=False)


# saves a check list in the checkboo 
# checklists have children models, whick might complicate my life :(
class ChecklistItem (models.Model) :
	id = models.AutoField(primary_key=True)
	checkbook = models.ForeignKey("Checkbook", related_name="checklists", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	last_edited = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=20, null=False, blank=False)


# check items for the check list
class CheckItem (models.Model):
	id = models.AutoField(primary_key=True)
	checklist = models.ForeignKey("ChecklistItem", related_name="items", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	checked = models.BooleanField(default=False)
	text = models.CharField(max_length=60, null=False, blank=False)