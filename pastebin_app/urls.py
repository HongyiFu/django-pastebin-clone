from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root, name='root'),
    url(r'^paste/$', views.paste, name='paste'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<rand_url>\S{10})/$', views.show, name='show'),
    url(r'^(?P<rand_url>\S{10})/delete$', views.delete, name='delete'),
]