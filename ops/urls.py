"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from ops.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^init/$', init),
    url(r'^login/$', Login, name='login'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^lockscreen/$', lockscreen),
    # url(r'^terminal/$', web_terminal),
    url(r'^setting/$', setting, name='setting'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^404/$', page404),
    url(r'^500/$', page500),
    url(r'^help/$', help, name='help'),

    url(r'^admin/', admin.site.urls),

    # 路由转发
    url(r'^users/', include('users.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^mysql/', include('mysql.urls')),
    # url(r'^library/', include('library.urls')),
    # url(r'^tools/', include('tools.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)