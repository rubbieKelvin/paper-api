from django.db import models
from rest_framework.request import Request
from django.core.validators import MinLengthValidator

# Create your models here.
class Checkbook (models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20, validators=[MinLengthValidator(3, "length of characters is too small")])
	starred = models.BooleanField(default=False)
	tags = models.ManyToManyField("Tag", through="TagMembership")

	date_created = models.DateTimeField(auto_now_add=True)
	date_edited  = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.name

	@staticmethod
	def get_checkbox_model_with_membership(request: Request, checkbook_id: int = None) -> tuple:
		checkbook_id: int = checkbook_id or request.data.get("checkbook_id")

		if checkbook_id == None: return None, None

		checkbook = Checkbook.objects.filter(id=checkbook_id).first()
		if checkbook == None: return False, False

		checkbook_membership = CheckbookMembership.objects.filter(user=request.user, checkbook=checkbook).first()
		if checkbook_membership == None: return checkbook, False

		return checkbook, checkbook_membership
	

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

	def __str__(self):
		return f"{self.id}: {self.title}"

	@staticmethod
	def get_textitem_model(request: Request, checkbook: Checkbook, textitem_id: int = None):
		id: int = textitem_id or request.data.get("textitem_id")
		if id == None: return None

		textitem = TextItem.objects.filter(id=id, checkbook=checkbook).first()

		if not textitem: return False
		return textitem


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


class Tag (models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=10)
	date_created = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.name

class TagMembership(models.Model):
	id = models.AutoField(primary_key=True)
	tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
	checkbook = models.ForeignKey("Checkbook", on_delete=models.CASCADE)
