from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import Record


class RecordListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        qs = Record.objects.filter(
            action__user=self.request.user
        )
        return qs
