from dashboard.models import ActionDashboardManager
from django.contrib.auth import get_user_model
from django.db import models
from statistic.models import ActionMonthStatisticManager

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   editable=True)

    class Meta:
        ordering = ('-created',)
        abstract = True


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

    objects = models.Manager()
    dashboard = ActionDashboardManager()
    month_statistic = ActionMonthStatisticManager()

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
