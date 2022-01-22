from django.db import models


CASHBACK_TYPE = (
    ("upto", "upto"), 
    ("flat", "flat"), 
)


class Store(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    logo = models.ImageField(upload_to='images/store_logo',default ='common/placeholder.png')
    tagline = models.CharField(max_length=100, blank=True, null=True)
    cashback_percent = models.PositiveSmallIntegerField(null=False, blank=False)
    cashback_type =  models.CharField(max_length=5, choices=CASHBACK_TYPE, default='upto') 
    affiliate_link = models.URLField(null=False, blank=False)
    category = models.ManyToManyField(to='common.Category',blank=True)
    brands = models.ManyToManyField(to='common.Brand',blank=True)

    def __str__(self):
        return self.name
    
    
class DealsCoupon(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    categories = models.ManyToManyField(to='common.Category',blank=True)
    brands = models.ManyToManyField(to='common.Brand',blank=True)
    store = models.ForeignKey(to='affiliate.Store',on_delete=models.SET_NULL,null=True, blank=True)
    coupon_code = models.CharField(max_length=100,blank=True, null=True)
    affiliate_link = models.URLField(null=False, blank=False)
    

    
class Product(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(to='common.Category',on_delete=models.SET_NULL,null=True, blank=True)
    brand = models.ForeignKey(to='common.Brand',on_delete=models.SET_NULL,null=True, blank=True)
    

class ProductPrice(models.Model):
    product = models.ForeignKey(to='affiliate.Product', on_delete=models.CASCADE, default=None, related_name='prices')
    store = models.ForeignKey(to='affiliate.Store', on_delete=models.CASCADE)
    cashback = models.PositiveSmallIntegerField(null=False, blank=False)
    cashback_type =  models.CharField(max_length=5, choices=CASHBACK_TYPE, default='upto') 
    standard_price = models.FloatField(null=False, blank=False)
    sale_price = models.FloatField(null=False, blank=False)
    affiliate_link = models.URLField(null=False, blank=False)
    
    

    def save(self, *args, **kwargs):
        self.standard_price = round(self.standard_price, 2)
        self.sale_price = round(self.sale_price, 2)
        super(ProductPrice, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.title


class ProductImage(models.Model):
    product = models.ForeignKey(to='affiliate.Product', on_delete=models.CASCADE, default=None, related_name='images')
    image = models.ImageField(upload_to='images/product_images', null=False, blank=False)
    def __str__(self):
        return self.product.title



 
