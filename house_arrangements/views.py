from django.views.generic import TemplateView, ListView, UpdateView, View
from django.views.generic.edit import CreateView
from django.forms import modelform_factory
from django.http import HttpResponse

from .models import House, Person


class IndexView(TemplateView):
    extra_context = {
        'houses': House.objects.all(),
        'people': Person.objects.filter(house__id=None)
    }
    template_name = 'index.html'

    def post(self, req, *args, **kwargs):
        person_id = req.POST.get('person')
        house_id = req.POST.get('house')
        spot = req.POST.get('spot')
        try:
            House.objects.get(house_id).add_person(person_id, spot)
            return HttpResponse('')
        except:
            return HttpResponse(f'Tried to move {person_id} to spot {spot} in {house_id}', status=403)

class HouseMixin:
    success_url = '/houses/'
    model = House
    fields = ['__all__']

class HousesList(HouseMixin, ListView):
    template_name = "house_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = modelform_factory(model=self.model, fields=self.fields)
        return context

class HouseCreate(HouseMixin, CreateView):
    pass

class HousesView(View):
    def get(self, request, *args, **kwargs):
        return HousesList.as_view()(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return HouseCreate.as_view()(request, *args, **kwargs)

class HouseView(HouseMixin, UpdateView):
    template_name = 'house_detail.html'
