# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from models import Reservation
from serializer import ReservationSerializer
from rest_framework.response import Response
from rest_framework.status import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import User
class ReservationAPI(APIView):
    # Gets a reservation
    # Within a range provided request has
    # start_date and end_date args
    # A specific reservation based on uuid
    # A reservations with default values.
    def get(self, request, uuid, format = None):
        start = request.GET.get("start")
        end = request.GET.get("end")
        if start != None and end != None:
            list_reservations = Reservation.get_reservation_range(start, end)
            serialized_list = ReservationSerializer(list_reservations, many=True)
            return Response(serialized_list.data, status=HTTP_200_OK)
        elif uuid:
            try:
                reservation = Reservation.objects.get(uuid=uuid)
            except ObjectDoesNotExist as E:
                return Response({"error":E.message}, status=HTTP_404_NOT_FOUND)
            serialized = ReservationSerializer(reservation)
            return Response(serialized.data, status=HTTP_200_OK)
        else:
            serialized = Reservation.get_reservation_range()
            # data = {}
            # data['start_date'] = datetime.fromtimestamp(serialized.data['start_date']).isoformat()
            # data['end_date'] = datetime.fromtimestamp(serialized.data['end_date']).isoformat()
            return Response(serialized.data, status=HTTP_200_OK)

    # Post is to confirm the reservation.
    def post(self, request, uuid, format = None):
        fullname, email = request.data["fullname"], request.data["email"]
        try:
            user = User.objects.get(email = email)
        except ObjectDoesNotExist as E:
            user = User.objects.create_user(
                username = email,
                first_name = fullname.split(" ")[0],
                last_name = fullname.split(" ")[-1],
                email = email
            )
        serialized = ReservationSerializer(data = request.data)
        if serialized.is_valid():
            try:
                reserved = serialized.save()
                reserved = reserved.reserve(user)
                serialized = ReservationSerializer(reserved)
                return Response(serialized.data, status=HTTP_201_CREATED)
            except Exception as E:
                return Response(E.message, status=HTTP_406_NOT_ACCEPTABLE)

        return Response(serialized.errors, status=HTTP_417_EXPECTATION_FAILED)

    # Modifies the reservation.
    # Need to add check if modification can is valid
    def put(self, request, uuid, format = None):
        reservation = Reservation.objects.get(uuid = uuid)
        serialized = ReservationSerializer(reservation, data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=HTTP_202_ACCEPTED)
        return Response(serialized.errors, status= HTTP_417_EXPECTATION_FAILED)

    # Deletes the reservation
    def delete(self, request, uuid, format = None):
        try:
            reservation = Reservation.objects.get(uuid = uuid)
            reservation.delete()
            return Response({"message": "Reservation {uuid} deleted.".format(uuid = uuid)}, status=HTTP_200_OK)
        except ObjectDoesNotExist as E:
            return Response({"error":ObjectDoesNotExist.message}, status=HTTP_404_NOT_FOUND)

