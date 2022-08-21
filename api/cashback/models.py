from django.db import models
from pkg_resources import require


class CashbackLevel(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    percentage = models.PositiveIntegerField(null=False, blank=False)
    required_minimum_after_sale_total = models.PositiveIntegerField(null=False, blank=False,default=0)
    fixed_distribution_percentage = models.PositiveIntegerField(null=False, blank=False)
    ratio_distribution_percentage = models.PositiveIntegerField(null=False, blank=False)
    date_created	= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_edited = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return str(self.name)
