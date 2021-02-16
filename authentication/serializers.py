from . models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		read_only_fields = (
			'id',
			'email',
			'is_active',
			'is_staff',
			'date_joined',
			"is_superuser",
			'last_login',
			"is_anonymous")

		fields = (
			*read_only_fields,
			*(
				'last_name',
				'first_name',
			)
		)
