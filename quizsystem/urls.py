from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.user_login_view, name="login"),
    path('home/', views.Home_view.as_view(), name="home"),
    path('application_form/', views.Application_Form_View.as_view(), name="application_form"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="quizsystem/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="quizsystem/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="quizsystem/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="quizsystem/password_reset_done.html"),
         name="password_reset_complete"),

]
