from django.db import models
from rooms.models import Room
from guests.models import Guest

class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, default='Booked')

    def __str__(self):
        return f"{self.guest} - {self.room}"