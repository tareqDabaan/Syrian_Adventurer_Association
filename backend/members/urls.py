from django.urls import path, include
from members import views
from rest_framework.routers import DefaultRouter

app_name = "members"

router = DefaultRouter()
router.register('', views.MemberViewSet)


urlpatterns = [
    
    
    # ------------------------------- Landing Page ------------------------------- #

    path('our_team/', views.OurTeam.as_view()), #? Display the members in 'our team' section    
    path('member_details/<int:member_id>', views.MemberActivityAPIView.as_view()), #? Display the member in 'Member' section    

    # ------------------------------- End Landing Page ------------------------------- #

    
    # ------------------------------ Admin Dashboard ----------------------------- #

    path('addmember/', views.CreateMember.as_view()),
    path('crud_members/', include(router.urls)),
    path('members_id/', views.MembersID.as_view()),

    # ------------------------------ End Admin Dashboard ----------------------------- #





    path('data/', views.analyze_member_ages),


]