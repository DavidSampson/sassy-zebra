from django.contrib import admin
from django.urls import path
from house_arrangements.views import Index, List, Update, Create, Detail, People, Houses, Spots


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="index"),
    path('houses/', List.as_view(), name="house_list"),
    path('houses/create/', Create.as_view(), name="house_create"),
    path('houses/<int:pk>/', Detail.as_view(), name="house_detail"),
    path('houses/<int:pk>/update', Update.as_view(), name="house_update"),
    path('api/people/', People.as_view(), name="people_api"),
    path('api/spots/', Spots.as_view(), name="spots_api"),
    path('api/houses/', Houses.as_view(), name="houses_api")
]
