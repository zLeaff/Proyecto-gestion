from django.urls import path
from .views import UserSignIn, UserLogout, ChangePasswordView, RequestPasswordResetView, ResetPasswordView

urlpatterns = [
    path('sign_in/', UserSignIn.as_view(), name='sign_in'),
    path('logout/', UserLogout, name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('request_reset_password/', RequestPasswordResetView.as_view(),
         name='request_reset_password'),
    path('reset_password/', ResetPasswordView, name='reset_password'),
]
