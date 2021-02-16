from . import views
from django.urls import path

urlpatterns = [
	path("checkbook/", views.CheckbookView.as_view())
]