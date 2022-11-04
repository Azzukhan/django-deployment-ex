from django.urls import path, include
from basicapp import views

app_name = 'basicapp'

urlpatterns = [
    path('register/',views.register,name = 'register'),
    path('login/',views.user_login,name='user_login')
]
