from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_view
from account import views

app_name = 'account'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.profileView, name='profile_update'),

    path('login/', auth_view.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('password_reset/', auth_view.PasswordResetView.as_view(
            template_name='account/password_reset.html',
            email_template_name = 'account/password_reset_email.html',
            success_url=reverse_lazy('account:password_reset_done')),
            name='password_reset'
            ),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
            template_name='account/password_reset_done.html'),
            name='password_reset_done'
            ),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html',
            success_url='/account/reset/done'),
            name='password_reset_confirm'
            ),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html'),
            name='password_reset_complete'
            ),

    path('password_change/', auth_view.PasswordChangeView.as_view(
            template_name='account/password_change.html',
            success_url=reverse_lazy('account:profile')),
            name='password_change'
            ),

]
