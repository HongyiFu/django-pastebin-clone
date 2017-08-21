from django.db import models

class Post(models.Model):
    name = models.CharField(db_index=True, max_length=300, blank=False)
    content = models.TextField()
    generated_url = models.CharField(db_index=True, max_length=10, blank=False)
 