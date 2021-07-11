from django.db import models
from django.utils.html import format_html
# Create your models here.
class Reports(models.Model):
    image = models.ImageField(upload_to='report_screenshot',default='default')
    name = models.CharField (max_length=80)
    email = models.EmailField(max_length=254)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    # display the image in the admin panel row.
    def image_tag(self):
        if self.image.url:
            return  format_html('<a href="{0}"><img src="{0}" width="30" height="30"/></a>'.format(self.image.url))
        return  'no image'
        
    #this is the requred fields to up and runner
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.email

class Reply(models.Model):
    reporter_email = models.EmailField(max_length=254)
    reporter_name = models.CharField(max_length=50)
    reply_body = models.TextField()
    reply_time = models.DateTimeField(auto_now_add=True)


