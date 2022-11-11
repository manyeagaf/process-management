from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('comment/<str:request_id>/', views.comment_create, name='comment'),
    path('create/', views.request_create, name='request-create'),
    path('<str:request_id>/assign/', views.assign_request, name='request-assign'),
    path('submitted/', views.getsubmitted, name="datatable"),
    path("close/<str:request_id>/",views.close_request,name='request-close'),
    path("open/<int:pk>/",views.open_request,name='request-open'),
    path("<int:request_id>/",views.request_detail,name='request-detail'),
]
