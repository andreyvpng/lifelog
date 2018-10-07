from calendar import monthrange

from dashboard.models import ActionDashboardManager
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   editable=True)

    class Meta:
        ordering = ('-created',)
        abstract = True


class ActionManager(models.Manager):

    def get_month_statistic(self, id, user, month, year):
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


class Action(TimeStampedModel):
    text = models.CharField(max_length=140)
    unit = models.CharField(max_length=50)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='actions')
    COLORS = (
        (1, 'orange'),
        (2, 'red-orange'),
        (3, 'radical-red'),
        (4, 'gray'),
        (5, 'green'),
        (6, 'blue'),
        (7, 'purple'),
    )
    color = models.IntegerField(
        choices=COLORS,
        default=1,
    )

    objects = ActionManager()
    dashboard = ActionDashboardManager()

    def __str__(self):
        return '{} ({})'.format(self.text[:75],
                                self.unit)


class Record(TimeStampedModel):
    action = models.ForeignKey(Action,
                               on_delete=models.CASCADE,
                               related_name='records')
    value = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.value,
                              self.action.unit[:75])
