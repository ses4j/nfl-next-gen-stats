from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('nfl_next_gen_stats.urls')),
    path('admin/', admin.site.urls),
]
