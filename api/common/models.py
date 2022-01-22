from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='images/categories',default ='common/placeholder.png')
    parent_category = models.ForeignKey(to='common.Category',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    
        
class Brand(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    logo = models.ImageField(upload_to='images/brand_logo',default ='common/placeholder.png')
    tagline = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
        