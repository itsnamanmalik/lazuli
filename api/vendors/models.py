from functools import total_ordering
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.users.models import UserCashbackLevel
from api.cashback.models import CashbackLevel
from django.db.models import F
from django.db import IntegrityError
import threading
from django.db import transaction

class Vendor(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    business_name = models.CharField(blank=True,null=True,max_length=100)
    business_type = models.CharField(blank=True,null=True,max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=False, blank=False,max_length=10, unique=True)
    password = models.CharField(blank=False,null=False,max_length=100)
    address = models.TextField(null=False, blank=False, max_length=150)
    wallet = models.FloatField(null=False, blank=False, default=0)
    gst_number = models.CharField(blank=True,null=True,max_length=50)
    commission_percentage = models.FloatField(null=False, blank=False, default=0)
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
    product_name = models.CharField(max_length=100,null=False, blank=False)
    total_amount = models.FloatField(null=False,blank=False,default=0)
    after_sale_total = models.FloatField(null=False,blank=False,default=0)
    marketing_fee_paid = models.BooleanField(null=False,blank=False,default=False)
    cashback_credited = models.BooleanField(null=False,blank=False,default=False)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_edited = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    
    

def update_cashback(created,instance):
    if created:
        before_vendors = VendorSale.objects.filter(date_created__lt=instance.date_created)
        for vendor in before_vendors:
            vendor.after_sale_total = vendor.after_sale_total+instance.total_amount
            vendor.save()
    else:
        all_cashback_levels = CashbackLevel.objects.all()
        for cashback_level in all_cashback_levels:
            if instance.after_sale_total >= cashback_level.required_minimum_after_sale_total:
                try:
                    with transaction.atomic():
                        user_cashback_level = UserCashbackLevel(user=instance.user,sale=instance,cashback_level=cashback_level)
                        user_cashback_level.save()
                except IntegrityError:
                    pass
                

@receiver(post_save, sender=VendorSale)
def update_cashback_level(sender, instance, created, **kwargs):
    th = threading.Thread(target=update_cashback(created,instance), args=(), kwargs={})
    th.start()
    th.join()
    
        
            
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
