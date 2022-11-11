from django.urls import path
from . import views

app_name = 'officer'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('active/',views.active,name='active-requests'),
    path('pending/',views.pending,name='pending-requests'),
    path('assigned/',views.assigned,name='assigned-requests'),
    path('closed/',views.closed,name='closed-requests'),
    path('requests/<str:request_id>/',views.request_detail,name = 'request-detail'),
]