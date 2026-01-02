from django.db import models

# Create your models here.
class CurrentOffer(models.Model):
    title = models.TextField()
    description = models.TextField()
    expiryDate = models.DateTimeField()
    keyImages = models.TextField()
    productLink = models.TextField()
    productSlug = models.TextField()