from rest_framework import fields
from . import models
from rest_framework.serializers import ModelSerializer

class CheckbookSerializer (ModelSerializer):
	class Meta:
		model = models.Checkbook
		fields = "__all__"


class CheckbookMembershipSerializer (ModelSerializer):
	checkbook = CheckbookSerializer()

	class Meta:
		model = models.CheckbookMembership
		fields = "__all__"