from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(login)
admin.site.register(staff)
admin.site.register(department)
admin.site.register(course)
admin.site.register(student)
admin.site.register(party)
admin.site.register(election)
admin.site.register(panel)
admin.site.register(panel_specific)
admin.site.register(election_panel)
admin.site.register(symbol)
admin.site.register(candidate)
admin.site.register(result)
admin.site.register(vote)

