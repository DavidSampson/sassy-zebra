from django.db import models
from django.core.exceptions import ValidationError

class Person(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class House(models.Model):
    name = models.CharField(max_length=200)

    max_bed_spots = models.IntegerField(default=0)
    bed_spots = models.ManyToManyField(Person, blank=True)

    max_floor_spots = models.IntegerField(default=0)
    floor_spots = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        return self.name

    def _clean_spots(self, limit, spot_list):
        if len(spot_list) > limit:
            raise ValidationError('Too many people in this spot!')

    def clean(self):
        self._clean_spots(self.max_bed_spots, self.bed_spots)
        self._clean_spots(self.max_floor_spots, self.floor_spots)

    def add_person(self, person, spot):
        if spot.startswith('bed'):
            self.bed_spots.add(person)
        elif spot.startswith('floor'):
            self.floor_spots.add(person)
        else:
            raise ValidationError('Spot type not valid')
        self.clean()
        self.save()
