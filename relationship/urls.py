from django.conf.urls import url
from relationship import views

urlpatterns = [
    url(r'^friendlist$', views.FriendList.as_view()),
	url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^magic$', views.magic),
    url(r'^msgouter$', views.msgrouter),
    url(r'^sendmsg$', views.sendmsg),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]