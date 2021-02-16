from paper.models import AudioItem, CheckItem, ChecklistItem
from rest_framework import fields
from rest_framework.fields import ImageField
from . import models
from rest_framework.serializers import ModelSerializer

class CheckbookSerializer (ModelSerializer):
	"""For little info."""
	class Meta:
		model = models.Checkbook
		fields = "__all__"


class CheckbookMembershipSerializer (ModelSerializer):
	checkbook = CheckbookSerializer()

	class Meta:
		model = models.CheckbookMembership
		fields = "__all__"


class TextItemSerializer (ModelSerializer):
	class Meta:
		model = models.TextItem
		fields = "__all__"


class ImageFieldSerializer(ModelSerializer):
	class Meta: 
		model = models.ImageItem
		fields = "__all__"


class AudioItemSerializer (ModelSerializer):
	class Meta:
		model = models.AudioItem
		fields = "__all__"


class CheckItemSerializer (ModelSerializer):
	class Meta:
		fields = "__all__"
		model = models.CheckItem


class ChecklistItemSerializer(ModelSerializer):
	items = CheckItemSerializer(many=True)
	class Meta:
		fields = "__all__"
		model = models.ChecklistItem


class CheckbookSerializerFull (ModelSerializer):

	texts = TextItemSerializer(many=True)
	images = ImageFieldSerializer(many=True)
	voicenotes = AudioItemSerializer(many=True)
	checklists = ChecklistItemSerializer(many=True)

	class Meta:
		model = models.Checkbook
		fields = "__all__"