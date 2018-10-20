from core.models import Action
from rest_framework import serializers


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Action
        fields = ('id', 'text', 'unit', 'user')
