from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(
    RoomType,
    on_delete=models.CASCADE,
    related_name='rooms',
    null=True,
    blank=True
)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"Room {self.number} ({self.status})"

    class Meta:
        ordering = ['number']