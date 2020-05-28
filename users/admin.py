from django.contrib import admin
from users.models import Fundoo

# Register your models here.

admin.site.register(Fundoo)
admin.site.site_header = 'FUNDOO APPLICATION'
