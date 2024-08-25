from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard_view'),
    path('log-food/', log_food, name='log_food'),
    path('logout/', logout_view, name='logout'),
    path('update-profile/', update_profile_view, name='update_profile'),
]

