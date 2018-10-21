from rest_framework import permissions
from core.models import Action


class IsOwnerOfAction(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            action_id = request.data.get('action')
            try:
                action = Action.objects.filter(id=action_id).first()
                return action.user == request.user
            except AttributeError:
                return False
        return True
