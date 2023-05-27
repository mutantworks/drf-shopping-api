from rest_framework import serializers

from .models import Order, OrderItem
from product.serializers import ProductSerializer


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['price', 'product', 'quantity']


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id', 'owner', 'first_name', 'last_name', 'email', 'address', 'zipcode', 'place', 'phone', 'items',
                  'paid_amount']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id', 'owner', 'first_name', 'last_name', 'email', 'address', 'zipcode', 'place', 'phone', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            print(item_data)
            print(item_data['product'].price)
            item_data['price'] = item_data['product'].price
            OrderItem.objects.create(order=order, **item_data)
        return order


class OrderChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'address', 'zipcode', 'place', 'phone', ]
