from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import Game
from .serializers import GameSerializer


class GameFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )
    platform = django_filters.CharFilter(
        field_name="platform", lookup_expr="iexact"
    )

    class Meta:
        model = Game
        fields = ["platform", "min_price", "max_price"]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by("-created_at")
    serializer_class = GameSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GameFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
