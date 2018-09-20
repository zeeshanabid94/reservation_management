from rest_framework.serializers import *
from models import Reservation

# This class is responsible for
# serializing and deserializing
# data in reservation objects
class ReservationSerializer(Serializer):
    user = ReadOnlyField(source = "user.id", required=False)
    start_date = IntegerField(required=False)
    end_date = IntegerField(required=False)
    check_in = ReadOnlyField()
    check_out = ReadOnlyField()
    uuid = UUIDField()

    def create(self, validated_data):
        return Reservation(**validated_data)

    def update(self, instance, validated_data):
        for key in validated_data:
            instance.modify(key, validated_data[key])
        instance.save()
        return instance


