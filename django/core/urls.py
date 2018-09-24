from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
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
]
