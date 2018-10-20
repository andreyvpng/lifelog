from core.models import Action
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    record_sum = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    def get_record_sum(self, obj):
        try:
            return obj.record_sum
        except AttributeError:
            return None

    def get_goal(self, obj):
        try:
            return {
                'id': obj.goal.id,
                'daily_value': obj.goal.daily_value
            }
        except ObjectDoesNotExist:
            return None

    class Meta:
        model = Action
        fields = ('id', 'text', 'unit', 'user', 'record_sum',
                  'goal')
