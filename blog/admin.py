from django.contrib import admin

from blog.models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ['title']}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
