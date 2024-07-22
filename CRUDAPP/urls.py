from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('index/<int:id>/', views.show_index, name='show_index'),
    path('', views.user_index), 
    path('index/', views.show_index, name='index'),
    path('login/', views.show_login, name='login'),
    path('logout/', views.show_logout, name='logout'),
    path('sign-up/', views.show_signup),
    path('pwrdreset/', views.show_pwrdreset, name='password_reset'),
    path('profile/', views.show_profile),
    path('edit-profile/', views.edit_profile),
    path('post-delete/<int:id>/', views.post_delete),
    path('post-edit/<int:id>/', views.post_edit),
    path('single-post/<int:id>/', views.single_post),
]
