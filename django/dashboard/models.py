from django.db import models


class ActionDashboardManager(models.Manager):

    def get(self, user, year, month, day):
        qs = self.get_queryset()
        qs = qs.filter(user=user)

        qs = qs.annotate(
            record_sum=models.aggregates.Sum(
                models.Case(
                    models.When(
                        records__created__day=day,
                        records__created__month=month,
                        records__created__year=year,
                        then=models.F('records__value')
                    ),
                    output_field=models.PositiveIntegerField(),
                    default=0
                )
            ),
        )
        return qs
