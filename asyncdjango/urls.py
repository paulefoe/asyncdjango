"""asyncdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
import datetime

from asgiref.sync import sync_to_async
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.contrib.auth.models import User
import aiohttp


@sync_to_async
def get_username():
    user = User.objects.last()
    return user.username


async def current_datetime(request):
    now = datetime.datetime.now()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/facts/cat') as resp:
            data = await resp.json()

    username = await get_username()
    html = f"<html><body>Hey, {username}, it is now {now}. " \
        f"Here's your random cat fact: {data['fact']}</body></html>"
    return HttpResponse(html)

urlpatterns = [
    path('', current_datetime,),
    path('admin/', admin.site.urls),
]
