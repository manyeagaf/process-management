from django.urls import path
from . import views

app_name = 'admin_user'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('active/',views.active,name='active-requests'),
    path('pending/',views.pending,name='pending-requests'),
    path('open/',views.open,name='open-requests'),
    path('closed/',views.closed,name='closed-requests'),
    path('requests/<str:request_id>/',views.request_detail,name = 'request-detail'),
    path('request-to-assign/<str:request_id>/',views.request_assign,name='request-assign'),
    path('archieved/',views.archieve,name='archieved'),
    # path('',views.admin,name='dashboard'),
    # path('<str:slug>/',views.admin,name = 'category'),
    
]