from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

class User(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=False, blank=False,max_length=10, unique=True)
    wallet = models.FloatField(null=False, blank=False, default=0)
    # user_id = models.CharField(max_length=20, null=False, blank=False)
    referral_id = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    notification_id = models.CharField(max_length=500, default="",null=False, blank=True)
    date_joined	= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        self.wallet = round(self.wallet, 2)
        super(User, self).save(*args, **kwargs)


TRANSACTION_TYPE = (
    ("debited", "debited"), 
    ("credited", "credited"), 
)

class UserCashbackLevel(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE,related_name='cashback_levels')
    sale = models.ForeignKey(to='vendors.VendorSale', on_delete=models.CASCADE)
    cashback_level = models.ForeignKey(to='cashback.CashbackLevel', on_delete=models.CASCADE)
    given_cashback = models.FloatField(null=False, blank=False, default=0)
    cashback_given = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user','sale','cashback_level',)
    def save(self, *args, **kwargs):
        if self.given_cashback:
            self.given_cashback = round(self.given_cashback, 2)
            if self.given_cashback < 0:
                self.given_cashback = 0
        super(UserCashbackLevel,self).save(*args, **kwargs)   

class UserWalletTransaction(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, default='debited') 
    cashback_level = models.ForeignKey(to='users.UserCashbackLevel', on_delete=models.SET_NULL,null=True, blank=True)
    is_cashback_transaction = models.BooleanField(default=False,null=False, blank=False)
    amount = models.FloatField(null=False, blank=False)
    paid_for = models.CharField(max_length=100,null=False, blank=False)
    transaction_breakdown = models.TextField(null=True, blank=True)
    time_date = models.DateTimeField(default=datetime.now,null=False,blank=False)
  
    def __str__(self):
        return self.user.phone+"-->"+self.transaction_type
    
    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        if self.amount < 0:
            self.amount = 0
        super(UserWalletTransaction,self).save(*args, **kwargs)


@receiver(post_save, sender=UserWalletTransaction)
def update_balance(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_type == 'debited': 
            instance.user.wallet = instance.user.wallet - instance.amount
            instance.user.save()
        elif instance.transaction_type == 'credited':
            instance.user.wallet = instance.user.wallet + instance.amount
            instance.user.save()
            
        if instance.cashback_level:
            instance.is_cashback_transaction = True
            instance.save()
            total_sale_cashback = UserWalletTransaction.objects.filter(cashback_level__sale = instance.cashback_level.sale).aggregate(Sum('cashback_level__given_cashback'))['cashback_level__given_cashback__sum']
            instance.cashback_level.sale.cashback_given = total_sale_cashback
            instance.cashback_level.sale.save()
            if total_sale_cashback >= instance.cashback_level.sale.total_amount:
                instance.cashback_level.sale.cashback_credited = True
                instance.cashback_level.sale.save()
                

