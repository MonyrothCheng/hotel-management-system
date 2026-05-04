from rest_framework import serializers
from .models import Room, RoomType

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    room_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'room_type_id', 'status']