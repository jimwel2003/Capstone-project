from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'BioFarmula'
admin.site.index_title = 'BioFarmula Admin'
admin.site.site_title = 'BioFarmula Information System'

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
