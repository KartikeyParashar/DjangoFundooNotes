from django.contrib import admin
from .models import Note, Label

# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_title')

    def user_title(self, obj):
        return obj.title

    def get_queryset(self, request):
        queryset = super(NoteAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-user')
        return queryset

    user_title.short_description = 'Title'


admin.site.register(Note, NoteAdmin)
admin.site.register(Label)
