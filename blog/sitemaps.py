from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # A custom sitemap

    # indicate the change frequency of your post pages
    # and their relevance in your website (the maximum value is 1)
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        # The items() method returns the QuerySet of objects to include in this sitemap.
        # by default, Django calls the get_absolute_url() method on each object to retrieve its URL.
        # Both the changefreq and priority attributes can be either methods or attributes.
        # If you want to specify the URL for each object, you can add a location method to your sitemap class. 
        return Post.published.all()

    def lastmod(self, obj):
        # Returns the last time the object was modified
        return obj.updated
