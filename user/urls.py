
from django.urls import path
from . import views as users_views
from blog.views import UserPostListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', users_views.register ,name="register"),
    path('profile/', users_views.profile ,name="profile"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html") ,name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html",next_page='login') ,name="logout"),

    path('<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html") ,name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html") ,name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html") ,name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html") ,name="password_reset_complete"),

]