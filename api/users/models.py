from django.db import models
from datetime import datetime  


class User(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=False, blank=False,max_length=10, unique=True)
    wallet = models.FloatField(null=False, blank=False, default=0)
    user_id = models.CharField(max_length=20, null=False, blank=False, unique=True)
    referral_id = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    cashback_level = models.ForeignKey(to='cashback.CashbackLevel',on_delete=models.SET_NULL, null=True, blank=True)
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


class UserWalletTransaction(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length = 20, choices = TRANSACTION_TYPE, default='debited') 
    amount = models.FloatField(null=False, blank=False)
    paid_for = models.CharField(max_length=100,null=False, blank=False)
    time_date = models.DateTimeField(default=datetime.now,null=False,blank=False)
    def __str__(self):
        return self.user.phone+"-->"+self.transaction_type
