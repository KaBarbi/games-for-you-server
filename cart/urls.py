from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register("cart", CartViewSet, basename="cart")
router.register("cart/items", CartItemViewSet, basename="cart-items")

urlpatterns = router.urls
