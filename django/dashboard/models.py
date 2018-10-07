from django.db import models
from django.db.models.aggregates import Sum


class ActionDashboardManager(models.Manager):

    def get(self, user, year, month, day):
        qs = self.get_queryset()
        qs = qs.filter(user=user)
        qs = qs.filter(
            records__created__day=day,
            records__created__month=month,
            records__created__year=year
        )
        qs = qs.annotate(
            record_sum=Sum('records__value'))
        return qs
