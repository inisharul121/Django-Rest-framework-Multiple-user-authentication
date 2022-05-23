
from django.urls import path
from .views import FreelanceSignupView,ClientSignupView,CustomeAuthToken,FreelancerOnlyView,ClientOnlyView,LogoutView

urlpatterns = [
path('signup/freelance/',FreelanceSignupView.as_view()),
path('signup/client/',ClientSignupView.as_view()),
path('login/',CustomeAuthToken.as_view(), name= 'auth_token'),
path('freelance/dashboard/',FreelancerOnlyView.as_view(), name= 'only_freelance'),
path('client/dashboard/',ClientOnlyView.as_view(), name= 'only_client'),
path('logout/',LogoutView.as_view(), name= 'logout'),
]
