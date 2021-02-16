from re import error
from paper.models import Checkbook
from . import models
from . import serializers

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.utils import IntegrityError

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
# user can create check books which can contain
# 	- checklists
# 	- images
# 	- voiceotes
# 	- notes

# create checkbook
class CheckbookView(APIView):

	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	parser_classes = [JSONParser]

	def get(self, request: Request) -> Response:
		# gets all the checkbook by the user
		checkbooks = models.CheckbookMembership.objects.filter(user=request.user)
		checkbooks_sr = serializers.CheckbookMembershipSerializer(checkbooks, many=True)
		return Response(data=checkbooks_sr.data)

	def post(self, request: Request) -> Response:
		data: dict = request.data
		""" data should be like:
			{
				name: <str>,
				starred: <bool>
			}
		"""

		# create a new checkbook
		name: str = data.get("name", "")
		starred: bool = data.get("starred", False)

		if len(name) < 3:
			return Response(data=dict(
				error="length of name too small. should be >= 3 characters."
			), status=status.HTTP_400_BAD_REQUEST)

		try:
			checkbook = models.Checkbook(
				name=name,
				starred=starred)
			checkbook.save()

		except IntegrityError:
			return Response(dict(
				error="a checkbook with that name already exists"
			))

		# add role
		membership = models.CheckbookMembership(role="ON", checkbook=checkbook, user=request.user)
		membership.save()

		# sr
		sr = serializers.CheckbookSerializer(checkbook)
		return Response(data=sr.data)
	
	def delete(self, request: Request) -> Response:
		# delete a checkbook
		"""
		{
			checkbook_id: <int>
		}
		"""
		checkbook_id: int = request.data.get("checkbook_id")
		
		if checkbook_id == None:
			"""no id attached"""
			return Response(
				data=dict(error="this endpoint requires an id key"),
				status=status.HTTP_400_BAD_REQUEST
			)

		checkbook: models.Checkbook = models.Checkbook.objects.filter(id=checkbook_id).first()

		if not checkbook:
			"""doesnt exists"""
			return Response(
				data=dict(error="checkbook with the gieven id doesnt exist"),
				status=status.HTTP_404_NOT_FOUND
			)

		# check if user actually owns the checkbook
		checkbook_membership: models.CheckbookMembership = models.CheckbookMembership.objects.filter(checkbook=checkbook, user=request.user).first()
		
		if not checkbook_membership:
			"""this user is not a member os this checkbook"""
			return Response(data=dict(
				error="this user is not a member os this checkbook"
			), status=status.HTTP_401_UNAUTHORIZED)

		if not (checkbook_membership.role == "ON"):
			"""only owners can delete checkbooks"""
			return Response(data=dict(
				error="only owners can delete checkbooks"
			), status=status.HTTP_401_UNAUTHORIZED)

		checkbook.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)

	def patch(self, request: Request) -> Response:
		# edit checkbook details
		""" data should be like:
			{
				id: <int>
				name: <str>,
				starred: <bool>
			}
		"""
		data: dict = request.data
		id: int = data.get("checkbook_id")

		if id is None:
			# there's no specified id
			return Response(
				data=dict(
					eror="No specified checkbook_id."
				), status=status.HTTP_400_BAD_REQUEST
			)

		# just delete the id: key cuase we already stored it.
		# and we need the content of data to save/edit our model.
		try:
			# dont mind the vscode (pylance) error
			del data["checkbook_id"]
		except KeyError:
			pass

		checkbook: models.Checkbook = models.Checkbook.objects.filter(id=id).first()

		if not checkbook:
			return Response(
				data=dict(
					error="checkbook not found"
				), status=status.HTTP_404_NOT_FOUND
			)

		membership: models.CheckbookMembership = models.CheckbookMembership.objects.filter(checkbook=checkbook, user=request.user).first()

		if not membership:
			return Response(
				data=dict(
					error="authenticated user des not have access to this checkbook"
				)
			)

		name: str = data.get("name")
		starred: bool = data.get("starred")

		# do edit
		if name:
			checkbook.name = name
		
		if not (starred is None):
			checkbook.starred = starred

		if name or not (starred is None):
			checkbook.save()

		sr = serializers.CheckbookSerializer(checkbook)

		return Response(data=sr.data)

	def put(self, request: Request) -> Response:
		# create an item underthe checkbook
		return Response(dict(
			message=""
		))

