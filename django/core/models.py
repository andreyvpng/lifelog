import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   editable=True)

    class Meta:
        ordering = ('-created',)
        abstract = True


class ActionManager(models.Manager):

    def dasboard(self, user):
        qs = self.get_queryset()
        qs = qs.filter(user=user)
        qs = qs.annotate(
            record_sum=Sum('records__value'))
        qs = qs.filter(records__created__gte=(
            timezone.now() - datetime.timedelta(days=1)))
        return qs


class Action(TimeStampedModel):
    text = models.CharField(max_length=140)
    unit = models.CharField(max_length=50)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='actions')
    COLORS = (
        ('or', 'orange'),
        ('bt', 'bruschetta-tomato'),
        ('wm', 'watermelon'),
        ('bw', 'bay-wharf'),
        ('gr', 'green'),
        ('cc', 'clear-chill'),
        ('bg', 'bright-greek'),
    )
    color = models.CharField(
        max_length=2,
        choices=COLORS,
        default='or',
    )

    objects = ActionManager()

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
