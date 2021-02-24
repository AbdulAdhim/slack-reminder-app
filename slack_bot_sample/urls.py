"""slack_bot_sample URL Configuration

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
from django.contrib import admin
from django.urls import path
from bot import views as bot_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bot_views.index, name='index'),
    path('clear', bot_views.clear, name='clear'),
    path('api/hello', bot_views.hello, name='api_hello'),
    path('api/reply', bot_views.reply, name='api_reply')
]
