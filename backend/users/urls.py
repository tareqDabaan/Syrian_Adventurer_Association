from django.urls import path
from users import auth_views, views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

router = DefaultRouter()
router.register("list_user", views.ListData, basename='list_user'),
urlpatterns = [
    
    #* ------------------------- Authentication operations ------------------------ #
    path('signup/', auth_views.Signup.as_view(), name = 'signup'),
    path('verify_account/', auth_views.VerifyAccount.as_view(), name = 'verify_account'),
    path('login/', auth_views.LoginAPI.as_view()),
    path('resend_code/',auth_views.ReGenerateOTPCode.as_view(), name = 'resend_code'),
    path('change_password/',auth_views.ChangePassword.as_view(), name = 'change_password'),
    path('logout/', auth_views.LogoutAPI.as_view(), name = 'logout'),
    path('request_password_reset/', auth_views.RequestPasswordReset.as_view(), name = 'request_password_reset'),
    path('verify_reset_code/', auth_views.PasswordResetVerifyCode.as_view(), name = 'verify_reset_code'),
    path('confirm_new_password/', auth_views.PasswordReset.as_view(), name = 'confirm_new_password'),
    path('complete_profile/', auth_views.CompleteSignUp.as_view({'put': 'update'}), name = 'profiles'),
    #* ---------------------------- End Authentication --------------------------- #
    
    #* -------------------------------- User Profile ------------------------------- #
    path('userprofile/', views.UserProfile.as_view(), name='profile'),
    path('userprofile/update/', views.UserUpdateView.as_view(), name='profile'),
    #* -------------------------------- End User Profile ------------------------------- #
    
    #* ---------------------- CRUD operations on user's data for admin dashboard ---------------------- #
    path('list_participants_data/', views.ListParticipantsData.as_view()),
    #* ---------------------------- End CRUD operations --------------------------- #


    
    #* ---------------------------------- Testing --------------------------------- #

    path('logouttest/', auth_views.LogoutTest.as_view(), name = 'logout'),
    path('refresh_token/', auth_views.ExRefresh.as_view()),
    path('test_login/', auth_views.MyObtainTokenPairView.as_view(), name=''),
    path('test_refresh/', TokenRefreshView.as_view(), name=''),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    
    #* ---------------------------------- End Testing --------------------------------- #
    
]
urlpatterns += router.urls