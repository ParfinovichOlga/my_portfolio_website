from django.contrib import admin
from .models import *

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("title",)}
    list_filter = ("category", "tags", "date")
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}

admin.site.register(Tag)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CV)
admin.site.register(Course)
admin.site.register(Education)


