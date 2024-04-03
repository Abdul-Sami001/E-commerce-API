from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from rest_framework import status
from django.db.models import Count
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from .filters import ProductFilterSet
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    #filterset_fields = ['collection_id']
    filterset_class = ProductFilterSet
    search_fields = ['title', 'description']
    
    
    
    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {
                    "error": "product cannot be deleted because it is associated with order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super(ProductViewSet, self).destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("product")).all()
    serializer_class = CollectionSerializer

    
    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs["pk"])
        if collection.product_set.count() > 0:
            return Response(
                {
                    "error": "product cannot be deleted because it is associated with order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super(ProductViewSet, self).destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])    

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','patch' ,'delete'] 
     
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer    
        
        return CartItemSerializer
        
    def get_serializer_context(self):
         return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id= self.kwargs['cart_pk']).select_related('product') 
    


#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         obj = get_object_or_404(CartItem, pk=pk)
#         return obj

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer        