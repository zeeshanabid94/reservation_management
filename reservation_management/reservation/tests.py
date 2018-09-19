# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
import unittest
from models import Reservation
from serializer import ReservationSerializer
from errors import ClashError, NotMinimumOneDayError, NotWithinOneMonth
import time
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import thread

# Create your tests here.
class TestReservationModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name = "Zeeshan",
            last_name = "Abid",
            email = "zabid@usc.edu"
        )
        self.user2 = User.objects.create(
            username = "jumbo",
            first_name = "HEllo",
            last_name = "World",
            email = "hello@hotmail.edu"
        )
        one_day = 60 * 60 * 24
        self.reservation_1 = Reservation()
        self.reservation_2 = Reservation()
        self.reservation_3 = Reservation(start_date=time.time() + 4 * one_day,
                                         end_date = time.time() + 8 * one_day)
        self.reservation_4 = Reservation(start_date=time.time() + 2 * one_day,
                                         end_date = time.time() + 8 * one_day)
        self.reservation_5 = Reservation(start_date=time.time() + 2 * one_day,
                                         end_date = time.time() + 34 * one_day)
        self.reservation_not_min_one = Reservation(start_date=time.time() + 1 * one_day,
                                         end_date = time.time() + 34 * one_day)
        self.reservation_not_max_30 = Reservation(start_date=time.time() + 56 * one_day,
                                         end_date = time.time() + 82 * one_day)


    def test_unique_uuid(self):
        reservations = [Reservation() for i in range(10)]
        repeat = False
        for i in range(len(reservations)-1):
            for j in range(i+1, len(reservations)):
                if reservations[i].uuid == reservations[j].uuid:
                    repeat = True


        self.assertEqual(False, repeat)

    def test_reserve(self):
        self.reservation_1.reserve(self.user)
        res_3 = Reservation.objects.get(uuid = self.reservation_1.uuid)

        self.assertEqual(res_3.start_date, self.reservation_1.start_date)
        self.assertEqual(res_3.end_date, self.reservation_1.end_date)

    def test_reserve_clash(self):
        self.reservation_1.reserve(self.user)
        self.assertRaises(ClashError,self.reservation_2.reserve, user=self.user)
        self.assertRaises(ClashError, self.reservation_3.reserve,user=self.user)
        self.assertRaises(ClashError, self.reservation_4.reserve,user=self.user)
        self.assertRaises(ClashError, self.reservation_5.reserve,user=self.user)

        self.reservation_3.reserve
        self.assertRaises(ClashError, self.reservation_4.reserve,user=self.user)
        self.assertRaises(ClashError, self.reservation_5.reserve,user=self.user)
        self.assertRaises(ClashError, self.reservation_2.reserve,user=self.user)
        self.assertRaises(ClashError, self.reservation_1.reserve,user=self.user)

    def test_policies(self):
        self.assertRaises(NotMinimumOneDayError, self.reservation_not_min_one.reserve, user = self.user)
        self.assertRaises(NotWithinOneMonth, self.reservation_not_max_30.reserve, user = self.user)

    def test_get_range_reservation(self):
        one_day = 60 * 60 * 24
        current = int(time.time())
        start_date = current + 10 * one_day
        end_date = current + 20 * one_day

        reservation = Reservation(start_date=start_date, end_date=end_date)
        reservation.reserve(self.user)
        range = Reservation.get_reservation_range(start_date - 10*one_day, end_date + 10*one_day)
        self.assertEqual(len(range), 2)
        reservation.delete()

        start_date = current + 5 * one_day
        end_date = current + 10 * one_day

        reservation1 = Reservation(start_date=start_date, end_date=end_date)
        reservation1.reserve(self.user)

        start_date = current + 15 * one_day
        end_date = current + 20 * one_day

        reservation2 = Reservation(start_date=start_date, end_date=end_date)
        reservation2.reserve(self.user2)

        range = Reservation.get_reservation_range(start_date - 13 * one_day, end_date + 10 * one_day)
        self.assertEqual(len(range), 3)
        for r in range:
            self.assertEqual(True, r.can_reserve())
        reservation1.delete()
        reservation2.delete()

        start_date = current + 5 * one_day
        end_date = current + 10 * one_day

        reservation = Reservation(start_date = start_date, end_date = end_date)
        reservation.reserve(self.user)

        range = Reservation.get_reservation_range(start_date * 5*one_day, end_date + 10 * one_day)
        self.assertEqual(len(range), 1)
        self.assertEqual(range[0].start_date > end_date, True)

class TestReservationSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Zeeshan",
            last_name="Abid",
            password="Hello",
            email="zabid@usc.edu"
        )
        self.reservation_1 = Reservation()

    def test_serialize(self):
        serialized_obj = ReservationSerializer(self.reservation_1)

        self.assertEqual(serialized_obj.data["start_date"], self.reservation_1.start_date)
        self.assertEqual(serialized_obj.data["end_date"], self.reservation_1.end_date)
        self.assertEqual(serialized_obj.data["uuid"], str(self.reservation_1.uuid))

class TestReservationView(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Zeeshan",
            last_name="Abid",
            password="Hello",
            email="zabid@usc.edu"
        )
        self.reservation_1 = Reservation()
        self.reservation_2 = Reservation()

    def test_get_reservation(self):
        client = Client(enforce_csrf_checks="False")
        response = client.get("/reservations/")
        print response
        self.assertEqual(True, response is not None)
        self.assertEqual(True, type(response.data[0]["start_date"]) is int)
        self.assertEqual(True, type(response.data[0]["end_date"]) is int)

    def test_get_reservation_uuid(self):
        client = Client(enforce_csrf_checks="False")
        self.reservation_1.reserve(self.user)

        response = client.get("/reservations/{uuid}".format(uuid = self.reservation_1.uuid))
        # print response
        # print self.reservation_1.uuid
        self.assertEqual(True, response is not None)
        self.assertEqual(response.data["uuid"],str(self.reservation_1.uuid))

    def test_make_reservation(self):
        client = Client(enforce_csrf_checks="False")
        data = ReservationSerializer(self.reservation_2).data
        data["fullname"] = "Zeeshan Abid"
        data["email"] = "zabid@usc.edu"
        # print "data", data
        response = client.post("/reservations/",
                               data = data)
        # print response
        reservation = Reservation.objects.get(uuid = response.data["uuid"])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.reservation_2.uuid,reservation.uuid)
        self.assertEqual(self.reservation_2.start_date, reservation.start_date)
        self.assertEqual(self.reservation_2.end_date, reservation.end_date)

    def test_update_reservation(self):
        client = Client(enforce_csrf_checks="False")
        self.reservation_1.reserve(self.user)
        data = ReservationSerializer(self.reservation_1).data
        data["start_date"] = data["start_date"] + 60*60*24

        response = client.put("/reservations/{uuid}".format(uuid = str(data["uuid"])),
                              content_type="application/json",
                              data=json.dumps(data))
        reservation = Reservation.objects.get(uuid = data["uuid"])

        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.reservation_1.uuid, reservation.uuid)
        self.assertEqual(self.reservation_1.start_date + 60*60*24, reservation.start_date)
        self.assertEqual(self.reservation_1.end_date, reservation.end_date)

    def test_delete_reservation(self):
        self.reservation_1.reserve(self.user)

        client = Client(enforce_csrf_checks="False")
        response = client.delete("/reservations/{uuid}".format(uuid = str(self.reservation_1.uuid)))

        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, Reservation.objects.get, uuid=str(self.reservation_1.uuid))

    def test_date_range(self):
        start = int(time.time()) + 60*60*24*10
        end = int(time.time()) + 60*60*24 * 20

        client = Client(enforce_csrf_checks="False")
        response = client.get("/reservations/?start={start}&end={end}".format(
            start = start,
            end = end
        )
        )
        print response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["start_date"], start)
        self.assertEqual(response.data[0]["end_date"], end)

    def test_list_reservation(self):
        one_day = 60*60*24
        start_date = int(time.time()) + 10*one_day
        end_date = int(time.time()) + 20*one_day

        reservation = Reservation(start_date = start_date, end_date = end_date)

        reservation.reserve(self.user)

        client = Client(enforce_csrf_checks="False")
        response = client.get("/reservations/?start={start}&end={end}".format(
            start=start_date -  10*one_day,
            end=end_date + 20*one_day
            )
        )
        print response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)