from django.contrib import admin
from django.urls import path
from house_arrangements.views import Index, List, Update, Create, Detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="index"),
    path('houses/', List.as_view(), name="house_list"),
    path('houses/create/', Create.as_view(), name="house_create"),
    path('houses/<int:pk>/', Detail.as_view(), name="house_detail"),
    path('houses/<int:pk>/update', Update.as_view(), name="house_update")
]
