from core.models import Action
from rest_framework import serializers
from goal.serializers import GoalSerializer


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    record_sum = serializers.SerializerMethodField()
    goal = GoalSerializer(read_only=True)

    def get_record_sum(self, obj):
        try:
            return obj.record_sum
        except AttributeError:
            return None

    class Meta:
        model = Action
        fields = ('id', 'text', 'unit', 'user', 'record_sum',
                  'goal')
