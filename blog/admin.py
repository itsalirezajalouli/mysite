from django.contrib import admin
from .models import Comment, Post

@admin.register(Post)                                                               # same as admin.site.register()
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']                 # model fields to be displayed
    list_filter = ['status', 'created', 'publish', 'author']                        # filter for foreing keys only
    search_fields = ['title', 'body']                                               # apear when there's more than 1
    prepopulated_fields = { 'slug': ('title',) }                                    # automatic slug from title
    raw_id_fields = ['author']
    date_hierarchy = 'publish'                                                      
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_filed = ['name', 'email', 'body']
