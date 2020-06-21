
from django.contrib import admin
from django.urls import path
from django.urls import path
from first import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login,name='login'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('logout/', views.logout,name='logout'),
    path('error/', views.error,name='error'),
    path('reg/', views.reg,name='reg'),
    path('forgot/',views.forgot,name='forgot'),
]
