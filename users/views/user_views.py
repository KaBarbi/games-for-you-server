from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from ..serializers.user_serializers import MeResponseSerializer


@extend_schema(
    summary="Retorna os dados do usuário autenticado",
    description="Endpoint para obter as informações do usuário logado.",
    responses={
        status.HTTP_200_OK: MeResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Usuário não autenticado ou token inválido"
        ),
    },
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeResponseSerializer(request.user)
        return Response(serializer.data)
