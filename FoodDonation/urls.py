"""FoodDonation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path
from food import views
from django.contrib.auth.views import LoginView,LogoutView

admin.site.site_header = "Zero Food Admin"
admin.site.site_title = "Zero Food Admin Portal"
admin.site.index_title = "Welcome to Zero Food Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('ngoclick', views.ngoclick_view,name='ngoclick'),
    path('donarclick', views.donarclick_view,name='donarclick'),

    path('ngosignup', views.ngo_signup_view,name='ngosignup'),
    path('donarsignup', views.donar_signup_view,name='donarsignup'),
    path('ngologin', LoginView.as_view(template_name='ngologin.html')),
    path('donarlogin', LoginView.as_view(template_name='donarlogin.html')),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    path('ngo-dashboard', views.ngo_dashboard_view,name='ngo-dashboard'),
    path('ngo-donation', views.ngo_donation_view,name='ngo-donation'),
    path('ngo-notice', views.ngo_notice_view,name='ngo-notice'),
    path('claim-donation/<int:pk1>/<int:pk2>/<str:pk3>', views.claim_donation_view, name='claim-donation'),
    
    path('donar-dashboard', views.donar_dashboard_view,name='donar-dashboard'),
    path('donar-donation', views.donar_donation_view,name='donar-donation'),
    path('claimed-donation', views.claimed_donation_view,name='claimed-donation'),
    path('donar-donation-history', views.donar_donation_history_view,name='donar-donation-history'),

    path('aboutus', views.aboutus_view,name='aboutus'),
    path('contactus', views.contactus_view,name='contactus'),

]
