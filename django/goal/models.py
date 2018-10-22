from core.models import Action
from django.db import models
from utils.models import TimeStampedModel


class Goal(TimeStampedModel):
    action = models.OneToOneField(Action,
                                  on_delete=models.CASCADE,
                                  related_name='goal')
    daily_value = models.PositiveIntegerField(null=False,
                                              verbose_name="Daily Value",
                                              help_text="Enter a daily goal")

    def __str__(self):
        return 'Goal: {} {} {}'.format(
            self.action.text,
            self.daily_value,
            self.action.unit
        )
