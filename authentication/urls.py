from django.urls import path
from authentication.views import (
                                  RegisterView, VerifyEmail, LoginView, 
                                  TokenCheckApi, RequestPasswordResetEmailApiView,
                                  SetPasswordAPIView
                                  )
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
  
  path('register/', RegisterView.as_view(), name='register'),
  path('verify-email/', VerifyEmail.as_view(), name = 'verify-email'),
  path('login/', LoginView.as_view(), name = 'login'),
  path('refresh/token/', TokenRefreshView.as_view(), name = 'refresh'),
  path("request-email-reset/", RequestPasswordResetEmailApiView.as_view(), name = "request-email-reset" ),
  path('password-reset/<uidb64>/<token>/', TokenCheckApi.as_view(), name = 'password-reset-email'),
  path('reset-password-complete/', SetPasswordAPIView.as_view(), name= 'reset-password-complete'),


]