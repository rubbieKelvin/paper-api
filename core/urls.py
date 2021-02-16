from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    path('api/app/', include('paper.urls'))
]


# the code below is quite useless
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

@api_view(["POST"])
@parser_classes([JSONParser])
def sanity_test(request: Request) -> Response:
    print(request.data)
    return Response(data=dict(msg="hey"))

urlpatterns.append(
    path('test/sanitytest/', sanity_test)
)

# import for rendering media files in development
from .settings import DEBUG
from django.conf import settings
from django.conf.urls.static import static

# THE CODE BELOW IS NOT SUITABLE FOR PRODUCTION
# I"LL SWITCH TO AMAZON S3 BUCKET
if DEBUG:
	urlpatterns += static(
		settings.MEDIA_URL,
		document_root=settings.MEDIA_ROOT
	)