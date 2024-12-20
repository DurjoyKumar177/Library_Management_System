from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserAccountUpdateView, PassChangeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update_profile/', UserAccountUpdateView.as_view(), name='update_profile' ),
    path('password_change/', PassChangeView.as_view(), name='password_change'),
]