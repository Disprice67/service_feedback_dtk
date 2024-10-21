from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)

from django.urls import path, reverse_lazy


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
#     path('logout/',
#          LogoutView.as_view(template_name='users/logged_out.html'),
#          name='logout'),
]
