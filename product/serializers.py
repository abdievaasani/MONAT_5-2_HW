from rest_framework import serializers
from .models import Product
from .models import Category
from .models import Review
from django.db.models import Avg



class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:

        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        return category.product_set.count()



class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ProductListSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price category reviews rating'.split()

    def get_rating(self, product):
        return product.reviews.aggregate(avg=Avg('stars'))['avg']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


