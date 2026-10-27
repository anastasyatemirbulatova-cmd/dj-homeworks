from rest_framework.permissions import BasePermission


class IsAdvertisementOwner(BasePermission):
    """Разрешает изменение и удаление только автору объявления."""

    message = "Изменять и удалять объявление может только его автор."

    def has_object_permission(self, request, view, obj):
        return obj.creator_id == request.user.pk
