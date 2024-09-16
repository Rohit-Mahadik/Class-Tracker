from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboardstudent/', views.dashboard,name='dashboardstudent'),
	path('studentattendance/',views.view_attendance,name='studentattendance'),
	path('viewassignments/',views.view_assignments,name='viewassignments'),
	path('viewannouncement/',views.view_announcements,name='viewannouncement'),
	path('leave_planner/',views.leave_planner,name='leave_planner'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('studpasswordchange/', views.PasswordChange, name='studpasswordchange'),
]