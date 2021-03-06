from django.contrib import admin

from .models import Post, Comment, PostLike


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_visible')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostLike)
