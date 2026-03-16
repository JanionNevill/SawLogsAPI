from django.db import models
from django.db.models import SET_NULL

from reservations.models import Reservation


class Log(models.Model):

    SPECIES = [
        ("WALNUT", "Walnut"),
        ("CHERRY", "Cherry"),
        ("OAK", "Oak"),
        ("MAPLE", "Maple"),
        ("ASH", "Ash"),
        ("YEW", "Yew"),
        ("POPLAR", "Poplar"),
        ("BIRCH", "Birch"),
    ]

    GRADE = [
        ("VENEER", "Veneer"),
        ("FURNITURE", "Furniture"),
        ("CABINETRY", "Cabinetry"),
        ("CONSTRUCTION", "Construction"),
        ("FIREWOOD", "Firewood"),
    ]

    species = models.CharField(choices=SPECIES)
    diameter = models.IntegerField(verbose_name="Diameter (cm)")
    length = models.IntegerField(verbose_name="Length (cm)")
    grade = models.CharField(choices=GRADE)

    reservation = models.ForeignKey(
        Reservation, on_delete=SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.species} {self.id}"
