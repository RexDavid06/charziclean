from django.urls import path
from authsys import views

app_name = 'authsys'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout')

]