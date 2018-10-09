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

        NOT_CHOSEN = 'N'
        GOAL_PASSED = 'P'
        GOAL_NOT_PASSED = 'F'
        ANSWER_CHOICES = (
            (NOT_CHOSEN, ''),
            (GOAL_PASSED, 'Daily Goal passed'),
            (GOAL_NOT_PASSED, 'Daily Goal not passed yet'),
        )

        qs = qs.annotate(
            is_goal_passed=models.Case(
                models.When(
                    record_sum__gte=models.F('goal__daily_value'),
                    then=models.Value(GOAL_PASSED)
                ),
                models.When(
                    goal=None,
                    then=models.Value(NOT_CHOSEN)
                ),
                default=models.Value(GOAL_NOT_PASSED),
                output_field=models.CharField(max_length=1,
                                              choices=ANSWER_CHOICES)
            )
        )

        return qs
