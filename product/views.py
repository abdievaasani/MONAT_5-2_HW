from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from rest_framework import status
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer
)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewListSerializer(reviews, many=True).data
    return Response(data=data)



@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)



@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategoryListSerializer(categories, many=True).data
        return Response(data=data)
    
    elif request.method == 'POST':
        serializer = CategoryDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = CategoryDetailSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # step 1: collect product (Queryset)
        product = Product.objects.prefetch_related('reviews').all()

        # step 2: reformat product to list of dictionaries
        data = ProductListSerializer(product, many=True).data

        # step 3: return response
        return Response(data=data)
    
    elif request.method == 'POST':
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

