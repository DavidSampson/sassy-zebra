from django.contrib import admin
from .models import House, Person, Spot

admin.site.register(Person)
admin.site.register(House)
admin.site.register(Spot)
