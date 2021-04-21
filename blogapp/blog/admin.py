from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post, Category, about, Contact


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)


class aboutAdmin(SummernoteModelAdmin):
    summernote_fields = ('message',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(about, aboutAdmin)

