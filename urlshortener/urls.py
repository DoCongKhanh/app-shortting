from django.urls import path
from . import views

app_name = 'shortener'
urlpatterns = [
    # Home view
    path('', views.home_view, name='home'),
      
    path('<str:shortened_part>', views.redirect_url_view, name='redirect'),   
    path('login/', views.login_user, name='login'),
    path('logout/', views.loguot_User, name='logout'),
    path('register/', views.register_user, name='register'),
]