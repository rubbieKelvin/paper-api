from . import views
from django.urls import path

urlpatterns = [
	path("checkbook/", views.CheckbookView.as_view()),

	path("tags/", views.TagView.as_view()),
	path("tags/delete/<int:id>/", views.deleteTag),

	path("checkbook/items/text/", views.CheckbookTextItemView.as_view()),
	path("checkbook/items/text/delete/<int:checkbook_id>/<int:textitem_id>/", views.deleteTextItem),
]