from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsAdvertisementOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """Создание, просмотр, изменение и удаление объявлений."""

    queryset = (
        Advertisement.objects
        .select_related("creator")
        .order_by("-created_at")
    )
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Возвращает права доступа для текущего действия."""
        if self.action == "create":
            return [IsAuthenticated()]

        if self.action in (
            "update",
            "partial_update",
            "destroy",
        ):
            return [
                IsAuthenticated(),
                IsAdvertisementOwner(),
            ]

        return [AllowAny()]
