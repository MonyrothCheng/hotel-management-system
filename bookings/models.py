from django.db import models
from rooms.models import Room
from guests.models import Guest
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()

    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Checked-in', 'Checked-in'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Booked',
        db_index=True
    )

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in")

        overlapping = Booking.objects.filter(
            room=self.room,
            status__in=['Booked', 'Checked-in'],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        )

        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This room is already booked for selected dates.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.update_room_status()

    def get_total_days(self):
        return (self.check_out - self.check_in).days

    def get_total_price(self):
        days = self.get_total_days()
        if days < 1:
            raise ValidationError("Booking must be at least 1 night.")
        return Decimal(days) * self.room.room_type.price

    def update_room_status(self):
        self.room.status = 'Occupied'
        self.room.save()

    def __str__(self):
        return f"{self.guest} - Room {self.room} ({self.status})"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out__gt=models.F('check_in')),
                name='check_out_after_check_in'
            )
        ]
        indexes = [
            models.Index(fields=['room', 'check_in', 'check_out']),
        ]

class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    payment_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        # auto calculate payment
        if not self.total_amount:
            self.total_amount = self.booking.get_total_price()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"