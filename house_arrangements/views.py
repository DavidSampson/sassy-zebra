from django.views.generic import View, TemplateView, ListView, UpdateView, DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core import serializers
from django.core.exceptions import ValidationError
from django.contrib.staticfiles import finders

from .models import House, Person, Spot, SpotFormSet

class HouseMixin:
    model = House
    fields = ["name"]
    def form_valid(self, form):
        self.object = form.save()
        spots = SpotFormSet(self.request.POST, instance=self.object)
        if spots.is_valid():
            spots.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spots"] = SpotFormSet(instance=self.object if hasattr(self, 'object') else None)
        return context
    def get_template_names(self):
        return ["%s%s.html" % (self.model._meta.model_name, self.template_name_suffix)]

class List(HouseMixin, ListView):
    pass

class Create(HouseMixin, CreateView):
    pass

class Detail(HouseMixin, DetailView):
    pass

class Update(HouseMixin, UpdateView):
    pass

class Index(View):
    def get(self, req):
        return FileResponse(open(finders.find('html/index.html'),'rb'))
    def post(self, req):
        person_id = int(req.POST.get('person'))
        spot_id = int(req.POST.get('spot'))
        try:
            Person.objects.get(id=person_id).set_spot(spot_id)
            return HttpResponse('')
        except ValidationError:
            return HttpResponse(
                f'Tried to move {person_id} to spot {spot_id}', status=403)

class ExposeModelAsJSONView(MultipleObjectMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(serializers.serialize('json', self.get_queryset()), safe=False)

class People(ExposeModelAsJSONView):
    model = Person
class Spots(ExposeModelAsJSONView):
    model = Spot
class Houses(ExposeModelAsJSONView):
    model = House
