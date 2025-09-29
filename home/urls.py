from django.urls import path
from accounts import views
from home.views import dashboard


urlpatterns = [
    path('',views.login, name = "login"),
    path('dashboard',dashboard, name = "dashboard"),
    path('signup',views.signup, name = "signup"),
    path('verify_email',views.verify_email, name = "verify_email"),
    path('reset_pass',views.reset_pass, name = "reset_pass"),
    path('chk_verification_code',views.chk_verification_code, name = "chk_verification_code"),
    path('update_password',views.update_password, name = "update_password"),
    path('signout',views.signout, name = "signout"),
    
]