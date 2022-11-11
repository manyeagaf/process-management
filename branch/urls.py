from django.urls import path
from . import views

app_name = 'branch'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('active/',views.active,name='active-requests'),
    path('pending/',views.pending,name='pending-requests'),
    path('submitted/',views.submitted,name='submitted-requests'),
    path('closed/',views.closed,name='closed-requests'),
    path('requests/<str:request_id>/',views.request_detail,name = 'request-detail'),
]