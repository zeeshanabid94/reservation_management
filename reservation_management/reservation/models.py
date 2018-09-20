# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import time
import uuid
from errors import UUIDNotUniqueError, ClashError, NotMinimumOneDayError, NotWithinOneMonth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from sherlock import Lock
from datetime import datetime
locks = ["0-10-days", "10-20-days", "20-30-days"]

# These methods return epoch time
# for one_day, two_day_from_now
# and current time
def one_day():
    return 60*60*24
def two_day_later():
    return round_to_prev_checkout(int(time.time()) + 60*60*24*2)

def get_unix_time():
    return int(time.time())

def thirty_days_after():
    return round_to_next_checkout(two_day_later() + 30*24*60*60)

def round_to_next_checkout(end_date):
    date = datetime.fromtimestamp(float(end_date))
    date = date.replace(hour=23, minute=59)
    return time.mktime(date.timetuple())

def round_to_prev_checkout(start_date):
    date = datetime.fromtimestamp(float(start_date))
    date = date.replace(hour=00, minute=00)
    return time.mktime(date.timetuple())


# The reservation model.
# This is main consumeable object
# of this app
class Reservation(models.Model):
    user = models.OneToOneField(User, related_name="user", default=None) # User who has this reservation
    start_date = models.BigIntegerField(default=two_day_later) # start date of the reservation
    end_date = models.BigIntegerField(default=thirty_days_after) # end date of the reservation
    uuid = models.UUIDField(default=uuid.uuid4) # Unique ID to identify the reservation

    # Note: All time is stored in unix time (epoch time). This makes working internally easier.
    # The time can be cast to any time and timezone when it is displayed.
    # Hence, that logic can stay on the consuming end.

    @property
    def check_in(self):
        return datetime.fromtimestamp(self.start_date).isoformat()

    @property
    def check_out(self):
        return datetime.fromtimestamp(self.end_date).isoformat()
    # Given a start_date and end_date,
    # Returns a list of reservations between those dates.
    @classmethod
    def get_reservation_range(self, start_date = None, end_date = None):
        if start_date == None:
            start_date = round_to_prev_checkout(two_day_later())
        else:
            start_date = round_to_prev_checkout(start_date)

        if end_date == None:
            end_date = round_to_next_checkout(thirty_days_after())
        else:
            end_date = round_to_next_checkout(end_date)
        reservations_before = Reservation.objects.filter(end_date__gte = start_date).filter(start_date__lte = start_date)
        reservations_after = Reservation.objects.filter(start_date__lte = end_date).filter(end_date__gte = end_date)


        if reservations_before.count() != 0:
            start_date = sorted(reservations_before, key = lambda x: x.end_date, reverse=True)[0].end_date + one_day()

        if reservations_after.count() != 0:
            end_date = sorted(reservations_after, key = lambda x: x.start_date)[0].start_date - one_day()

        reservations_middle = Reservation.objects.filter(start_date__gte = start_date,
                                                         end_date__lte = end_date)

        if reservations_middle.count() != 0:
            intervals = map(lambda x: (x.start_date - one_day(), x.end_date+one_day()), sorted(reservations_middle, key = lambda x: x.start_date))

            open_intervals = []
            current = start_date

            for interval in intervals:
                open_intervals.append((current, interval[0]))
                current = interval[1]
            if current < end_date:
                open_intervals.append((current, end_date))
            list_open = []

            for open in open_intervals:
                reservation = Reservation(start_date = open[0], end_date = open[1])
                list_open.append(reservation)

            return list_open
        return [Reservation(start_date=start_date, end_date = end_date)]

    # Reserves the object by saving it to the database.
    # Here 'reserved' means if the entry gets 'saved'
    # This method is a critical section as it saves the reservation
    # making it final.
    # To handle concurrency, a distributed lock system is used.
    # The system is using memcached as the lock store,
    # and python package sherlock to manage locks.
    def reserve(self, user):
        locks = self.get_locks()
        locks = map(lambda x: Lock(x), locks)

        for lock in locks:
            lock.acquire()
        if self.can_reserve():
            self.user = user
            self.save()
            for lock in locks:
                lock.release()
        else:
            for lock in locks:
                lock.release()
            raise ClashError(self.start_date, self.end_date)
        return self

    # Returns list of locks to acquire to reserve
    # This returns the list of locks a thread has to acquire
    # in order to reserve a reservation.
    # The three lock scheme allows smaller reservations to happen
    # quicker than longer reservations.
    def get_locks(self):
        if self.start_date < 10 * one_day() + two_day_later() and \
            self.end_date < 10 * one_day() + two_day_later():
            return ["0-10-days"]
        elif self.start_date >= 10 * one_day() + two_day_later():
            if self.end_date < 20*one_day() + two_day_later():
                return ["10-20-days"]
            else:
                return ["10-20-days", "20-30-days"]
        elif self.start_date >= 20 * one_day() + two_day_later():
            return ["20-30-days"]
        elif self.end_date >= 20* one_day() + two_day_later():
            return ["0-10-days", "10-20-days", "20-30-days"]
        elif self.end_date >= 10 * one_day() + two_day_later():
            return ["0-10-days", "10-20-days"]

    # Modify the key to the particular value
    def modify(self, key, value):
        if key == "start_date":
            self.start_date = value
        elif key == "end_date":
            self.end_date = value
        return self

    # Tells if at the moment before save
    # Whether this date range is available
    def can_reserve(self):
        if not self.min_one_day():
            raise NotMinimumOneDayError(self)
        if not self.max_one_month():
            raise NotWithinOneMonth(self)
        if not self.no_overlaps():
            raise ClashError(self.start_date, self.end_date)

        return True

    def no_overlaps(self):
        clashes_supersets = Reservation.objects.filter(start_date__lte = self.start_date) \
                .filter(end_date__gte = self.end_date)

        clashes_overlaps_1 = Reservation.objects.filter(end_date__gte = self.start_date).filter(start_date__lte = self.start_date)
        clashes_overlaps_2 = Reservation.objects.filter(start_date__lte = self.end_date).filter(end_date__gte = self.end_date)

        total_count = clashes_supersets.count() + clashes_overlaps_1.count() + clashes_overlaps_2.count()
        if total_count == 0:
            return True
        else:
            return False

    # Makes sure the reservation requested for meets
    # restrictions
    def min_one_day(self):
        return self.start_date >= two_day_later()

    def max_one_month(self):
        return self.start_date <= (24*60*60*30) + two_day_later()


    def __str__(self):
        start = datetime.fromtimestamp(float(self.start_date))
        end = datetime.fromtimestamp(float(self.end_date))
        return "Reservation from {start} to {end}".format(start = start, end = end)


    # Check if the reservation exists.
    def is_reserved(self):
        try:
            Reservation.objects.get(uuid = self.uuid)
            return True
        except ObjectDoesNotExist as E:
            return False