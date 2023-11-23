from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_page, name="login-signup"),
    path("profile/<str:pk>/", views.user_profile, name= "profile"),
    path('create-account', views.sign_up,  name="create-account"),
    path("logout/", views.logout_page, name="logout"),
    path('delete-message/<str:pk>/', views.delete_message, name= "delete-message"),
    path('', views.home, name="home" ),
    path('room/<str:pk>/', views.room, name = "room"),
    path('edit-profile/<str:pk>/', views.edit_profile, name="edit-profile"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:pk>/", views.update_room, name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete-room")

]