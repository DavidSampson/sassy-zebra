from django.contrib import admin
from django.urls import path
from house_arrangements.views import IndexView, HousesView, HouseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('houses/', HousesView.as_view(), name="house_list"),
    path('houses/<int:pk>/', HouseView.as_view(), name="house_detail")
]
