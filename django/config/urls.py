"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import user.urls

import core.urls
import dashboard.urls
import goal.urls
import statistic.urls
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user.urls, namespace='user')),
    path('dashboard/', include(dashboard.urls, namespace='dashboard')),
    path('statistic/', include(statistic.urls, namespace='statistic')),
    path('goal/', include(goal.urls, namespace='goal')),
    path('', include(core.urls, namespace='core')),
    path('', RedirectView.as_view(url='/dashboard', permanent=True)),
]
