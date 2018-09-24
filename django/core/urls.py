from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('records',
         views.RecordListView.as_view(),
         name='record-list'),
]
