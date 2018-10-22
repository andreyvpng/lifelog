from dashboard.models import ActionDashboardManager
from django.contrib.auth import get_user_model
from django.db import models
from statistic.models import ActionMonthStatisticManager
from utils.models import TimeStampedModel

User = get_user_model()


class Action(TimeStampedModel):
    text = models.CharField(max_length=140,
                            null=False,
                            verbose_name="Text",
                            help_text="Enter an action title (e.g. Book Reading)")
    unit = models.CharField(max_length=50,
                            null=False,
                            verbose_name="Unit",
                            help_text="Enter a unit (e.g. pages)")

    user = models.ForeignKey(User,
                             null=False,
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
        verbose_name="Color",
        help_text="Choose a color of progress bar"
    )

    objects = models.Manager()
    dashboard = ActionDashboardManager()
    month_statistic = ActionMonthStatisticManager()

    def __str__(self):
        return '{} ({})'.format(self.text[:75],
                                self.unit)

    class Meta:
        verbose_name = 'action'
        verbose_name_plural = 'actions'
        ordering = ('-created', )


class Record(TimeStampedModel):
    action = models.ForeignKey(Action,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='records')
    value = models.PositiveIntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.value,
                              self.action.unit[:75])
