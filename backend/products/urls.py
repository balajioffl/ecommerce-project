from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
    AttributeViewSet,
    AttributeValueViewSet,
    ProductVariantViewSet,
    VariantAttributeViewSet,
)

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

router.register(
    "attributes",
    AttributeViewSet,
)

router.register(
    "attribute-values",
    AttributeValueViewSet,
)

router.register(
    "variants",
    ProductVariantViewSet,
)

router.register(
    "variant-attributes",
    VariantAttributeViewSet,
)


urlpatterns = router.urls
