from rest_framework.exceptions import APIException

class NoReservations(APIException):
    status_code = 404
    default_code = "no_reservations"
    default_detail = "No reservations found."
