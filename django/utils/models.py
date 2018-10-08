from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   editable=True)

    class Meta:
        ordering = ('-created',)
        abstract = True
