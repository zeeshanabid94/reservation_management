from datetime import datetime
class UUIDNotUniqueError(Exception):
    def __init__(self, uuid):
        self.message = "{uuid} is not unique for this reservation.".format(uuid)


class ClashError(Exception):
    def __init__(self, start_date, end_date):
        self.message = "Range {start_date} and {end_date} of dates"\
                       "already reserved".format(start_date = datetime.fromtimestamp(start_date),
                                                 end_date = datetime.fromtimestamp(end_date))

class NotMinimumOneDayError(Exception):
    def __init__(self, reservation):
        self.message = "INVALID Reservation: {res} \n Booking can be done 2 day in advance only." \
                        .format(res = reservation)
        self.reservation = reservation

class NotWithinOneMonth(Exception):
    def __init__(self, reservation):
        self.message = "Your reservation start date has to be with in one month of today."
        self.reservation = reservation