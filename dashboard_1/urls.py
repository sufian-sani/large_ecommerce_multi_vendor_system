"""dashboard_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve

admin.site.site_header = "BoomBoom Group Pvt. Ltd."
admin.site.site_title = "BoomBoom Group Admin Panel"
admin.site.index_title = "BoomBoom Group Admin Panel"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('login_register', include('user_login_register.urls')),
    path('deshboard/', include('app_1.urls')),
    path('checkout/', include('checkout.urls')),
    path('vendor_dashboard/', include('vendor_dashboard_app.urls')),
    path('campaign/', include('campaign.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

