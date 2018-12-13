from django.views.generic import TemplateView

from house_arrangements.models import Person, House

class Index(TemplateView):
    extra_context = {
        'houses': House.objects.all(),
        'people': Person.objects.filter(house__isnull=True)
    }
    template_name = 'index.html'
