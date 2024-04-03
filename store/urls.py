from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register(r"customers", views.CustomerViewSet)
router.register('carts', views.CartViewSet)
# router.register('cart_item/<id>', views.CartItemViewSet)
# urlpatterns = router.urls

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('item', views.CartItemViewSet, basename='cart-items')
urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(carts_router.urls)),
    #     path("product/<int:pk>", views.ProductDetailView.as_view()),
    #     path("collections", views.CollectionListView.as_view()),
    #     path("collection/<int:pk>", views.CollectionDetailView.as_view()),
]
