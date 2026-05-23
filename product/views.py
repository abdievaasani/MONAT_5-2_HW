from django.db.models import Avg, Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsModerator

from .models import Product, Category, Review
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
    ProductValidateSerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 5


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticatedOrReadOnly()]

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsModerator()]

        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ProductValidateSerializer
        return ProductSerializer