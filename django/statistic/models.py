from calendar import monthrange

from django.db import models
from django.db.models.aggregates import Sum


class ActionMonthStatisticManager(models.Manager):

    def get(self, id, user, month, year):
        qs = self.get_queryset()
        qs = qs.filter(user=user)
        qs = qs.filter(
        )

        list = []
        number_of_days = monthrange(year, month)[1]
        for day in range(1, number_of_days + 1):
            sum_for_day = qs.filter(
                id=id,
                records__created__month=month,
                records__created__year=year,
                records__created__day=day
            ).aggregate(Sum('records__value'))['records__value__sum']

            if sum_for_day is None:
                sum_for_day = 0

            list.append(sum_for_day)
        return list
