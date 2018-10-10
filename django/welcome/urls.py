from welcome import views
from django.urls import path

app_name = 'welcome'
urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome')
]
