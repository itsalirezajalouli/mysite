from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone 

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().filter(status = Post.Status.PUBLISHED))

class Post(models.Model):

    class Status(models.TextChoices):
        # Status.choices 
        # Status.names = Status.values, Status.labels
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Meta:
        ordering = ['-publish']
        indexes = [ models.Index(fields = ['-publish']) ]

    title = models.CharField(max_length = 250)                                      # VARCHAR SQL column
    slug = models.SlugField(max_length = 250,                                       # for urls
                            unique_for_date = 'publish')                            # enforce unique slugs in a date

    author = models.ForeignKey(                                                     # Many-to-One relation:
                                                                                    # 1 user, many posts
            settings.AUTH_USER_MODEL,                                               # default user model
            on_delete = models.CASCADE,                                             # if user x_x -> all posts x_x
            related_name = 'blog_posts',                                            # so we can use user.blog_posts
            )
    body = models.TextField()                                                       # TEXT SQL column
    publish = models.DateTimeField(default = timezone.now)                          # DATETIME column
    created = models.DateTimeField(auto_now_add = True)
    # only updated when saving the obj
    updated = models.DateTimeField(auto_now = True)   
    status = models.CharField(max_length = 2,
                              choices = Status,
                              default = Status.DRAFT)                               # it's an enum
    objects = models.Manager()                                                      # default manager 
    published = PublishedManager()                                                  # custom manager

    # django uses this method to represent the object in places like admin site
    def __str__(self) -> str:
        return str(self.title)

    # builds post urls in reverse (Database -> URL generation)
    # gets the query from user and if it's in the db it generates the url
    def get_absolute_url(self):                                                     
        return reverse(                                                             
                'blog:post_detail',                                                 # blog namespace def in urls.py
                args = [self.publish.year,                                          # builds url dynamically using
                        self.publish.month,                                         # urlpatterns in urls.py
                        self.publish.day,
                        self.slug]                                                  
                )                                                                   
