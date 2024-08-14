from django.db import models


class Item(models.Model):
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    expires_at = models.DateTimeField(db_index=True)
