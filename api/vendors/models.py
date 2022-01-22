from django.db import models

class Vendor(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    business_name = models.CharField(blank=True,null=True,max_length=100)
    business_type = models.CharField(blank=True,null=True,max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=False, blank=False,max_length=10, unique=True)
    address = models.TextField(null=False, blank=False, max_length=150)
    wallet = models.FloatField(null=False, blank=False, default=0)
    gst_number = models.CharField(blank=True,null=True,max_length=50)
    notification_id = models.CharField(max_length=500, default="",null=False, blank=True)
    date_joined	= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        self.wallet = round(self.wallet, 2)
        super(Vendor, self).save(*args, **kwargs)


class VendorSale(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(to='vendors.Vendor', on_delete=models.SET_NULL, null=True, blank=True)
    
# TRANSACTION_TYPE = (
#     ("debited", "debited"), 
#     ("credited", "credited"), 
# )


# class UserWalletTransaction(models.Model):
#     user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, null=False, blank=False,related_name='transactions')
#     transaction_type = models.CharField(max_length = 20, choices = TRANSACTION_TYPE, default='debited') 
#     amount = models.FloatField(null=False, blank=False)
#     paid_for = models.CharField(max_length=100,null=False, blank=False)
#     time_date = models.DateTimeField(default=datetime.now,null=False,blank=False)
#     def __str__(self):
#         return self.user.phone+"-->"+self.transaction_type