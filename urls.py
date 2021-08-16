from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index),

    url(r'^register$', views.register),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^login_captain$', views.login_captain),
    url(r'^logout$', views.logout),

    url(r'^command$', views.command),

    url(r'^command/add_Crew$', views.addCrew),
    url(r'^update_Attendance/', views.updateAttendance),
    url(r'^remove_Crew/(?P<crew_id>\d+)$', views.removeCrew),

    url(r'^command/add_Task$', views.addTask),
    url(r'^removeTask/(?P<task_id>\d+)$', views.removeTask),

    url(r'^command/update_Status/(?P<stat_id>\d+)$', views.updateStatus),

    url(r'^attendance', views.attendance),

]
