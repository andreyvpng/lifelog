from goal.models import Goal
from rest_framework import serializers


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    action = serializers.IntegerField(source='action.id')

    class Meta:
        model = Goal
        fields = ('id',
                  'daily_value',
                  'action')
