"""newtradeinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from gettrademail import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.indexp, name='index'),
    path('googleinfo/', views.googleinfo, name='googleinfo'),
    path('getweb/', views.getweb, name='getweb'),
    path('getpam/', views.getPaM, name='getpam'),
    path('getwebsource/', views.getWebSource, name='getwebsource'),
    path('get_mail_from_website/', views.get_mail_from_website, name='get_mail_from_website'),
    path('getyahoo/', views.getyahoo, name='getyahoo'),
    path('getask/', views.getAsk, name='getask'),
    path('getmail/', views.getnewmail, name='getmail'),
    path('tradeinfo/', views.tradeinfo, name='tradeinfo'),
    path('searchweb/', views.searchweb, name='searchweb'),
    path('getemail_from_keyid/', views.getemail_from_keyid, name='searchweb'),


    path('get_mail/', views.get_mail, name='get_mail'),
    path('get_web/', views.get_web, name='get_web'),

    path('exportindia/', views.exportindia, name='exportindia'),
    path('yellowpages_ph/', views.yellowpages_ph, name='yellowpages_ph'),
    path('europages/', views.europages, name='europages'),


    path('exportindia_get_total/', views.exportindia_get_total, name='exportindia_get_total'),
    path('yellow_page_nums/', views.yellow_page_nums, name='yellow_page_nums'),
    path('test/', views.test, name='test'),
    path('get_socials/', views.get_socials, name='get_socials'),
    path('get_web_new/', views.get_web_new, name='get_web'),

]
