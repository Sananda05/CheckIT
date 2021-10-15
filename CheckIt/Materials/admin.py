from django.contrib import admin
from .models import materials,Comment,course_list

# Register your models here.

admin.site.register(materials)
admin.site.register(course_list)
admin.site.register(Comment)


