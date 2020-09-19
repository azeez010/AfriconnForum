from django.conf.urls import url
from . import views
from .views import visit_profile
from django.urls import path
from . import functionalities
from .views import updateProfile

urlpatterns = [
    path("info/", views.info, name="info"),
    url(r'^$', views.home, name="home" ),
    path("profile/transactions/", views.transactions, name="transactions"),
    path("profile/report/", views.report_comment, name="report-comment"),
    path("profile/transfer-points/", views.transfer, name="profile-transfer"),
    path('profile/follow/', functionalities.follow, name="follow"),
    path("profile/theme/", functionalities.theme, name="theme"),  
    path("profile/update-profile/", views.update_profile, name="update-profile"),
    path("profile/<str:username>/", views.visit_profile, name="visit-profile"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/<int:pk>/", updateProfile.as_view(), name="update-profile"),
    path("reports/<str:obj_type>/<int:obj_id>/", views.report, name="report"),
    path("report/ban/<int:user_id>/<str:obj_type>/<int:obj_id>/", views.report_ban, name="report_ban"),
    path("report/seen/<str:obj_type>/<int:obj_id>/", views.report_seen, name="report_seen"),
    path("advertisement/", views.advertisement, name="advertisement"),
    path("your-ads/", views.your_ads, name="your_ads"),
    path("follower-page/", views.follower_page, name="follower-page"),
    path("followers-content/", views.followers_content, name="followers-content"),
    path("favourites/", views.favourites, name="favourites"),
    path("ads-approval/", views.ads_approval, name="ads-approval"),
    path("signin/", views.signin, name="signin"),
    path("approved/", functionalities.approved, name="approved"),
    path("reject/", functionalities.reject, name="reject"),
    path("message-admin/", functionalities.message_admin, name="message-admin"),
    path("remove-homethread/", functionalities.remove_homethread, name="remove-homethread"),
    path("remove-home/", functionalities.remove_home, name="remove-home"),
    path("your-followers/", views.your_followers, name="your-followers"),
    path("countrystats/", views.countrystats, name="countrystats"),
    path("check-followers-profile/<int:profile_id>/<str:profile_username>/", views.check_followers_profile, name="check-followers-profile")
]