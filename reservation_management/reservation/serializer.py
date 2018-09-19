from rest_framework.serializers import *
from models import Reservation

# This class is responsible for
# serializing and deserializing
# data in reservation objects
class ReservationSerializer(Serializer):
    user = ReadOnlyField(source = "user.id")
    start_date = IntegerField()
    end_date = IntegerField()
    uuid = UUIDField()

    def create(self, validated_data):
        return Reservation(**validated_data)

    def update(self, instance, validated_data):
        for key in validated_data:
            instance.modify(key, validated_data[key])
        instance.save()
        return instance


