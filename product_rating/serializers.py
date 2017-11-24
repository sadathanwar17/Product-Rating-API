from rest_framework import serializers
from .models import Product_Table, Product_User_Table
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Table
        fields = ('id','product_name','product_description', 'ratings_sum', 'ratings_count','ratings_average','product_quantity')
        read_only_fields = ('product_ratings','ratings_count','ratings_average','ratings_sum')

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_User_Table
        fields = ('product_id','product_name','product_ratings','product_quantity')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

