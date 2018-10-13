from django.urls import path
from goal import views

app_name = 'goal'
urlpatterns = [
    path('create/action/<int:pk>',
         views.GoalCreateView.as_view(),
         name='create'),
    path('update/action/<int:pk>',
         views.GoalUpdateView.as_view(),
         name='update')
]
