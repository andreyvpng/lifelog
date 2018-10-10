from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('',
         views.WelcomeView.as_view(),
         name='welcome'),
    path('records',
         views.RecordListView.as_view(),
         name='record-list'),
    path('record-create',
         views.RecordCreateView.as_view(),
         name='record-create'),
    path('actions',
         views.ActionListView.as_view(),
         name='action-list'),
    path('action-create',
         views.ActionCreateView.as_view(),
         name='action-create'),
    path('action-update/<int:pk>',
         views.ActionUpdateView.as_view(),
         name='action-update'),
    path('action-delete/<int:pk>',
         views.ActionDeleteView.as_view(),
         name='action-delete')
]
