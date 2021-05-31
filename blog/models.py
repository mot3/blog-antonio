from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class publishedManager(models.Manager):
    # Create another manager
    def get_queryset(self):
        # Filter the model just to get the published objects
        return super(publishedManager, self).get_queryset()\
            .filter(status='published')  # In the line we can see the filter


class Post(models.Model):
    # Create a list of status choices with key and value
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # Become to VarChar
    title = models.CharField(max_length=250)

    # Create slug for the better seo.
    # This field used in url.
    # The unique_for_date Are used so that we no longer have several slugs at the same time
    # in published time that we create in later.
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # We have a foreignkey between user model and post model.
    # The related_name for put special name in this connection.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    # Become to Text
    body = models.TextField()

    # Determine the timezone for each post
    publish = models.DateTimeField(default=timezone.now)

    # Determine the time when a post created
    created = models.DateTimeField(auto_now_add=True)

    # Determine the time for last update
    updated = models.DateTimeField(auto_now=True)

    # Determine the status of each post
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # Keep any additional information of each model.
        # Somehow all the specific features of a model are defined in this class.
        ordering = ('-publish',)

    def __str__(self) -> str:
        # Give a special name to each post
        return self.title

    # When want to add another manager, we had to determine object manager if want it
    objects = models.Manager()
    published = publishedManager()  # Add the second manager that we created in above

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug,
                       ])

    # The tags manager will allow you to add,
    # retrieve, and remove tags from Postobjects.
    tags = TaggableManager()


class Comment(models.Model):
    # If you don't define the related_name attribute,
    # Django will use the name of the model in lowercase,
    # followed by _set (that is, comment_set).
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'
