from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class House(models.Model):
    name = models.CharField(max_length=200)
    people = models.ManyToManyField(Person, blank=True)
    def __str__(self):
        return self.name
