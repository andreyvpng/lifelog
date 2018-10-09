from django.urls import path
from goal import views

app_name = 'goal'
urlpatterns = [
    path('create',
         views.GoalCreateUpdateView.as_view(),
         name='create')
]
