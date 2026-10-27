from django.contrib.auth import get_user_model
from rest_framework import serializers

from advertisements.models import (
    Advertisement,
    AdvertisementStatusChoices,
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        """Назначает текущего пользователя автором объявления."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Проверяет ограничение количества открытых объявлений."""
        instance = self.instance

        if instance is None:
            creator = self.context["request"].user
            current_status = AdvertisementStatusChoices.OPEN
        else:
            creator = instance.creator
            current_status = instance.status

        status = data.get("status", current_status)

        if status != AdvertisementStatusChoices.OPEN:
            return data

        open_advertisements = Advertisement.objects.filter(
            creator=creator,
            status=AdvertisementStatusChoices.OPEN,
        )

        if instance is not None:
            open_advertisements = open_advertisements.exclude(
                pk=instance.pk,
            )

        if open_advertisements.count() >= 10:
            raise serializers.ValidationError(
                {
                    "status": (
                        "У пользователя не может быть больше "
                        "10 открытых объявлений."
                    )
                }
            )

        return data
