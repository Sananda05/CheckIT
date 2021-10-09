from django.contrib import admin
from .models import materials,Comment,course_list

# Register your models here.

admin.site.register(materials)
admin.site.register(course_list)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'body', 'material', 'date_added', 'active')
    list_filter = ('active', 'date_added')
    search_fields = ( 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

