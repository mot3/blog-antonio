from django.contrib import admin
from .models import Post

# For use the default panel for admin
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Create custome admin panel.
    # This class makes full Inheritance of the default admin class. (amdin.ModelAdmin)

    # This fields show in posts, when we see all the posts
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # In the right column for filter
    list_filter = ('status', 'created', 'publish', 'author')

    # Specify the search filelds
    search_fields = ('title', 'body')

    # Automatic fulling the slug with tiltle
    prepopulated_fields = {'slug': ('title',)}

    # This is a special way to facilitate the search of users
    raw_id_fields = ('author',)

    # Add a toolbar search for date in publish date
    date_hierarchy = 'publish'

    # Create default ordering on
    ordering = ('status', 'publish')

