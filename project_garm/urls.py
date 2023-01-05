from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

from django.conf.urls.static import static
from django.conf import settings


from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True)), name='graphql'),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
