from django.db import models

class Category(models.Model):
    class Meta:
        db_table = 'category'
        default_permissions = ()
    
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return u'{0}'.format(self.name)

class Tag(models.Model):
    class Meta:
        db_table = 'tag'
        default_permissions = ()

    category = models.ForeignKey(Category, related_name='tags')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return u'{0}'.format(self.name)