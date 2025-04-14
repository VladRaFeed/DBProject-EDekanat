from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/update/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('workers/', views.worker_list, name='worker_list'),
    path('workers/create/', views.worker_create, name='worker_create'),
    path('workers/<int:pk>/update/', views.worker_update, name='worker_update'),
    path('workers/<int:pk>/delete/', views.worker_delete, name='worker_delete'),
]