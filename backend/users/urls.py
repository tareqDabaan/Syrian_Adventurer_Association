from django.urls import path
from users import auth_views, views
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register("list_user", views.Listdaa, basename='list_user')

urlpatterns = [
    
    # Authentication operations
    path('signup/', auth_views.Signup.as_view(), name = 'signup'),
    path('verify_account/', auth_views.VerifyAccount.as_view(), name = 'verify_account'),
    path('login/', auth_views.LogInAPI.as_view(), name = 'login'),
    path('resend_code/',auth_views.ReGenerateOTPCode.as_view(), name = 'resend_code'),
    path('change_password/',auth_views.ChangePassword.as_view(), name = 'change_password'),
    path('logout/', auth_views.LogoutAPI.as_view(), name = 'logout'),
    path('request_password_reset/', auth_views.RequestPasswordReset.as_view(), name = 'request_password_reset'),
    path('verify_reset_code/', auth_views.PasswordResetVerifyCode.as_view(), name = 'verify_reset_code'),
    path('confirm_new_password/', auth_views.PasswordReset.as_view(), name = 'confirm_new_password'),
    path('complete_profile/', auth_views.CompleteSignUp.as_view({'put': 'update'}), name = 'profiles'),


    # CRUD operations on user's data
    path('user_profile/', views.UserProfile.as_view()),

    path('member_profile/', views.ListMemberData.as_view()),


]

urlpatterns += router.urls