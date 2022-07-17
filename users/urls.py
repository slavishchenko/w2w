from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('log-out/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('add-to-watchlist/', views.add_to_watchlist, name='add-to-watchlist'),
    path('remove-from-watchlist/', views.rm_from_watchlist, name='rm-from-watchlist'),
    path('favourite/', views.favourite, name='favourite'),
    path('remove-favourite/', views.rm_favourite, name='rm-favourite'),
    path('<int:id>/<str:slug>/share-your-thoughts/', views.share_your_thoughts, name='share-your-thoughts'),
    path('<slug:slug>/', views.profile, name='profile'),
    path('<slug:slug>/settings/', views.settings, name='settings'),
]
