from django.urls import path
from . import views
app_name = "users"
urlpatterns = [
    # post views
    path('user-create/',views.create_user,name='user-create'),
    path('user-delete/<int:pk>',views.delete_user,name='user-delete'),
    path('user-privileges/create',views.create_user_privilege,name='privilege-create'),
    path('user-privileges/delete/<int:pk>/',views.delete_privilege,name='privilege-delete'),
    path('user-activate/<int:pk>',views.activate_user,name='user-activate'),
    path('privilege-activate/<int:pk>',views.activate_privilege,name='privilege-activate'),
    path('login/',views.user_login,name = 'login'),
    path('logout/',views.user_logout,name='logout'),
    
]
