from django.db import models
from django.forms import inlineformset_factory
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_between_ones(value):
    if value > 1 or value < -1:
        raise ValidationError(f'{value} is not between 1 and -1')

class House(models.Model):
    name = models.CharField(max_length=200)
    cats = models.BooleanField(null=True, default=None)
    dogs = models.BooleanField(null=True, default=None)
    noise = models.FloatField(validators=[validate_between_ones], null=True, default=None)
    early_up = models.FloatField(validators=[validate_between_ones], null=True, default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('house_detail', args=[str(self.id)])

class Spot(models.Model):
    SPOT_TYPES = (
        ('bed', 'Bed'),
        ('floor', 'Floor'),
        ('couch', 'Couch')
    )
    spot_type = models.CharField(max_length=200, choices=SPOT_TYPES)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    house = models.ForeignKey('House', on_delete=models.CASCADE)

SpotFormSet = inlineformset_factory(
    House,
    Spot,
    fields=("spot_type", "name", "description", "quantity"))

class Person(models.Model):
    name = models.CharField(max_length=200)
    spot = models.ForeignKey('Spot', on_delete=models.SET_NULL, null=True, default=None)
    cats = models.FloatField(validators=[validate_between_ones], null=True, default=None)
    dogs = models.FloatField(validators=[validate_between_ones], null=True, default=None)
    noise = models.FloatField(validators=[validate_between_ones], null=True, default=None)
    early_up = models.FloatField(validators=[validate_between_ones], null=True, default=None)
    bed = models.FloatField(validators=[validate_between_ones], null=True, default=None)

    def __str__(self):
        return self.name

    def set_spot(self, spot_id):
        if spot_id == -1:
            self.spot = None
        else:
            spot = Spot.objects.get(id=spot_id)
            if spot.person_set.count() + 1 > spot.quantity:
                raise ValidationError(f'Spot {spot.id} is full')
            else:
                self.spot = spot
        self.save()
