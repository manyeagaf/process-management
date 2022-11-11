from django.urls import path
from . import views

app_name = 'access_control'

urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('user-privileges/',views.privileges,name='user-privileges'), 
    path('pending-users',views.pending_user_creations,name='pending-users-creation'),
    path('pending-privileges',views.pending_privileges,name='pending-privileges') , 
    path('user-action/<int:pk>/',views.user_action,name="user-action"),
    path('pending-user-approve/<int:pk>/',views.pending_user_approve,name="user-approve"),
    path('pending-user-delete/<int:pk>/',views.pending_user_delete,name="user-delete"),
    path('privilege-action/<int:pk>/',views.privilege_action,name="privilege-action"),
    path('pending-privilege-approve/<int:pk>/',views.pending_privilege_approve,name="privilege-approve"),
]