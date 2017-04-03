from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /cases/
    url(r'^$', views.index, name='case_index'),
    # ex: /cases/create/
    url(r'^create/$', views.create, name='case_create'),
    # ex: /cases/edit/
    url(r'^(?P<case_id>[0-9]+)/edit/$', views.edit, name='case_edit'),
    # ex: /polls/5/update/
    url(r'^(?P<case_id>[0-9]+)/$', views.detail, name='case_detail'),
    # ex: /polls/5/update/
    url(r'^(?P<case_id>[0-9]+)/update/$', views.update, name='case_update'),
    # ex: /polls/5/comment/
    url(r'^(?P<case_id>[0-9]+)/comment/$', views.comment, name='case_comment'),
    # ex: /polls/5/delete/
    url(r'^(?P<case_id>[0-9]+)/delete/$', views.delete, name='case_delete'),
]