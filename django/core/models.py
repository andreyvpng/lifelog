from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Action(TimeStampedModel):
    text = models.CharField(max_length=140)
    unit = models.CharField(max_length=50)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='actions')

    def __str__(self):
        return '{} ({})'.format(self.text[:75],
                                self.unit)


class Record(TimeStampedModel):
    action = models.ForeignKey(Action,
                               on_delete=models.CASCADE,
                               related_name='records')
    values = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.values,
                              self.action.unit[:75])
