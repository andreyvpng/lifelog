from statistic import views
from django.urls import path

app_name = 'statistic'
urlpatterns = [
    path('<int:pk>',
         views.ActionCurrentMonthView.as_view(),
         name='current-month'),
    path('<int:pk>/<int:year>-<int:month>',
         views.ActionMonthView.as_view(),
         name='month')
]
