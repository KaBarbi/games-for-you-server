from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import GameViewSet
from cart.views import CartViewSet, CartItemViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

router = DefaultRouter()
router.register(r'games', GameViewSet, basename="game")
router.register(r'carts', CartViewSet, basename="cart")
router.register(r'cart-items', CartItemViewSet, basename="cartitem")

urlpatterns = [
    path("admin/", admin.site.urls),

    # api
    path("api/", include(router.urls)),
    path("api/users/", include("users.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
