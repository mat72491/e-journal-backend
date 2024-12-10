"""
URL configuration for EJournal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from main_app import views
from rest_framework_simplejwt import views as jwt_views
from main_app.views import get_tags

urlpatterns = [
    path('entries/', views.EntryListView.as_view(), name='entry-list'),
    path('entries/create/', views.EntryCreateView.as_view(), name='entry-create'),
    path('entries/<int:pk>/update/', views.EntryUpdateView.as_view(), name='entry-update'),  
    path('entries/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry-delete'),
    path('auth/register/', views.UserRegisterView.as_view(), name='user-register'),
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('tags/top/', views.get_top_tags, name='top_tags'),
    path('entries/recent/', views.get_recent_entries, name='recent_entries'),
    path('tags/', get_tags, name='tags-list'),
    path('admin/', admin.site.urls)
]
