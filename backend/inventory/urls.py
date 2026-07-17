from rest_framework.routers import DefaultRouter

from .views import InventoryTransactionViewSet

router = DefaultRouter()

router.register(
    "inventory-transactions",
    InventoryTransactionViewSet,
)

urlpatterns = router.urls