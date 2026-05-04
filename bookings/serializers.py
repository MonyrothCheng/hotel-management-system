from rest_framework import serializers
from .models import Booking, Payment

class BookingSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    room_number = serializers.CharField(source='room.number', read_only=True)
    total_days = serializers.ReadOnlyField(source='get_total_days')
    total_price = serializers.ReadOnlyField(source='get_total_price')

    class Meta:
        model = Booking
        fields = [
            'id',
            'guest',
            'guest_name',
            'room',
            'room_number',
            'check_in',
            'check_out',
            'status',
            'total_days',
            'total_price'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'