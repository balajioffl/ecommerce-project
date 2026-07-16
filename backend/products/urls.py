from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet,BrandViewSet, ProductViewSet, ProductImageViewSet

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "brands",
    BrandViewSet,
    basename="brand",
)

router.register(
    "products",
    ProductViewSet,
    basename="product",
)

router.register(
    "product-images",
    ProductImageViewSet,
    basename="product-image",
)


urlpatterns = router.urls
