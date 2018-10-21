from core.models import Action, Record
from goal.serializers import GoalSerializer
from rest_framework import serializers


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


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    action = serializers.PrimaryKeyRelatedField(queryset=Action.objects.all())

    class Meta:
        model = Record
        fields = ('value', 'action')
