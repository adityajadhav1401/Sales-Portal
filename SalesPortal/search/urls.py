from django.urls import include,path
from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	re_path(r'^photos/(?P<path>.*)$', views.protected_serve, {'document_root': settings.MEDIA_ROOT}),
	path('search/',views.search_view, name = 'search_view'),
	path('result/',views.result_view, name = 'result_view'),
]