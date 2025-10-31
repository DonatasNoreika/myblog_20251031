from django.contrib import admin
from .models import Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'author']
    inlines = [CommentInLine]

admin.site.register(Post, PostAdmin)
