from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    image = models.ImageField(upload_to='images/cities', default ='common/logo.png')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"