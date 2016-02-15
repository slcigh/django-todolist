from django.conf.urls import url
from do import views

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^add_task/(?P<project_name>[\w\-]+)$', views.add_task, name='add_task'),
               url(r'^task_filter/$', views.task_filter, name='task_filter'),
               url(r'^change_task/(?P<project_name>[\w\-]+)/(?P<task_id>[\d]+)$', views.change_task_finish,
                   name='change_task_finish'),
               url(r'^edit_task/$', views.edit_task, name='edit_task'),
               url(r'^del_task/(?P<project_name>[\w\-]+)/(?P<task_id>[\d]+)$', views.delete_task,
                   name='delete_task'),
               url(r'^register/$', views.register, name='register'),
               url(r'^login/$', views.user_login, name='login'),
               url(r'^logout/$', views.user_logout, name='logout'),]
