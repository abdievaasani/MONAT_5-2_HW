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

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value
    
    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Отзыв слишком короткий")
        return value


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

    def validate_name(self, name):
        if len(value) < 2:
            raise serializers.validationError("Название слишком короткое")
        return value 




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

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value
    
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название слишком короткое")
        return value


