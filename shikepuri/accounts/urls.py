from django.conf.urls import url
from django.contrib.auth.views import login, logout
from accounts import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^regist_save/$', views.regist_save, name='regist_save'),
    url(r'^login/$', login,
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'},
        name='logout')
]
