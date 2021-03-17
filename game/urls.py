from django.urls import path

from . import views


app_name = 'game'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('create_game/', views.createGame, name='create_game'),
    path('demand/<int:game_id>', views.createDemand, name='demand'),
    path('role/<int:role_id>', views.enterGame, name='enterGame')
]