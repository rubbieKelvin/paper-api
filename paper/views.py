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
from rest_framework.decorators import api_view, permission_classes, parser_classes, authentication_classes

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
		# create an item under the checkbook
		return Response(dict(
			message=""
		))


class TagView(APIView):

	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]
	parser_classes = [JSONParser]

	def get(self, request: Request) -> Response:
		"""show all tags belonging to the user"""
		user = request.user
		tags = models.Tag.objects.filter(owner=user)
		tags_sr = serializers.TagSerializer(tags, many=True)

		return Response(data=tags_sr.data)

	def post(self, request: Request) -> Response:
		"""Create a new tag"""
		user = request.user
		name: str = request.data.get("name")

		if name:
			tag = models.Tag(name=name, owner=user)
			tag.save()

			tag_sr = serializers.TagSerializer(tag)
			return Response(data=tag_sr.data)

		return Response(data=dict(
			error="name value not provided"
		), status=status.HTTP_400_BAD_REQUEST)
	

@api_view(["DELETE"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteTag(request: Request, id: int) -> Response:
	"""Delete a tag"""
	user = request.user

	if not (id is None):
		tag = models.Tag.objects.filter(owner=user, id=id).first()

		if tag:
			tag.delete();
			
		return Response(status=status.HTTP_204_NO_CONTENT)

	return Response(dict(
		error="tag id was not provided"
	), status=status.HTTP_404_NOT_FOUND)


class CheckbookTextItemView(APIView):
	parser_classes = [JSONParser]
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]

	def get(self, request: Request) -> Response:
		"""returns all the text-items belonging to the specified checkbook"""
		checkbook, checkbook_membership = models.Checkbook.get_checkbox_model_with_membership(request)

		if not (checkbook is None):

			if checkbook:

				if checkbook_membership:
					text_items = models.TextItem.objects.filter(checkbook=checkbook)
					text_items_sr = serializers.TextItemSerializer(text_items, many=True)
					return Response(text_items_sr.data)
				else:
					Response(dict(error="not permitted to read this"), status=status.HTTP_401_UNAUTHORIZED)
			else:
				Response(dict(eror="no such checkbook", status=status.HTTP_404_NOT_FOUND))

		return Response(dict(error="checkbook_id not specified"), status=status.HTTP_400_BAD_REQUEST)

	def post(self, request: Request) -> Response:
		"""create a new text-item for the specified checkbook"""
		checkbook, membership = models.Checkbook.get_checkbox_model_with_membership(request)

		if not (checkbook is None):
			if (checkbook):
				if (membership):
					title = request.data.get("title", "")
					content = request.data.get("content")

					if not title:
						return Response(dict(error="note title is empty"), status=status.HTTP_400_BAD_REQUEST)

					if not content:
						return Response(dict(error="note content is empty"), status=status.HTTP_400_BAD_REQUEST)

					textitem = models.TextItem(checkbook=checkbook, text=content, title=title)
					textitem.save()

					textitem_sr = serializers.TextItemSerializer(textitem)
					return Response(textitem_sr.data)
				else:
					return Response(dict(error="not permitted to edit this check book"), status=status.HTTP_401_UNAUTHORIZED)
			else:
				return Response(dict(error="checkbook with the given id does not exist"), status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(dict(error="checkbook_id not specified"), status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request: Request) -> Response:
		"""edit the specified text-item"""
		checkbook, membership = models.Checkbook.get_checkbox_model_with_membership(request)

		if not (checkbook is None):
			if (checkbook):
				if (membership):
					textitem: models.TextItem = models.TextItem.get_textitem_model(request, checkbook)

					if textitem == None:
						return Response(dict(error="textitem_id is not specified"), status=status.HTTP_400_BAD_REQUEST)
					
					if not textitem:
						return Response(dict(error="textitem not found"), status=status.HTTP_404_NOT_FOUND)

					title = request.data.get("title", "")
					content = request.data.get("content")

					if title:
						textitem.title = title

					if content:
						textitem.text = content

					textitem.save()
					textitem_sr = serializers.TextItemSerializer(textitem)
					return Response(textitem_sr.data)
				else:
					return Response(dict(error="not permitted to edit this check book"), status=status.HTTP_401_UNAUTHORIZED)
			else:
				return Response(dict(error="checkbook with the given id does not exist"), status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(dict(error="checkbook_id not specified"), status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteTextItem(request: Request, checkbook_id: int, textitem_id: int) -> Response:
	checkbook, membership = models.Checkbook.get_checkbox_model_with_membership(request, checkbook_id)
	if not (checkbook is None):
		if (checkbook):
			if (membership):
				textitem: models.TextItem = models.TextItem.get_textitem_model(request, checkbook, textitem_id=textitem_id)
				
				if textitem == None:
					return Response(dict(error="textitem_id is not specified"), status=status.HTTP_400_BAD_REQUEST)
				
				if not textitem:
					return Response(dict(error="textitem not found"), status=status.HTTP_404_NOT_FOUND)

				textitem.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)
			else:
				return Response(dict(error="not permitted to edit this check book"), status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response(dict(error="checkbook with the given id does not exist"), status=status.HTTP_404_NOT_FOUND)
	else:
		return Response(dict(error="checkbook_id not specified"), status=status.HTTP_400_BAD_REQUEST)
