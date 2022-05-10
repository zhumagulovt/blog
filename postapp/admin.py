from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ckeditor.widgets import CKEditorWidget

from .models import Post, Category, Comment


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_author', 'created_at', 'updated_at')

    def link_to_author(self, obj):
        link = reverse('admin:auth_user_change', args=[obj.author_id])
        return format_html('<a href="{}">{}</a>', link, obj.author.username)

    link_to_author.short_description = 'Автор'
    form = PostAdminForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)