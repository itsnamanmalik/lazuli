from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from api.users.models import UserWalletTransaction

STATUS = (
    ("pending", "pending"), 
    ("approved", "approved"), 
)


class CashbackRequest(models.Model):
    user = models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    order_proof = models.ImageField(upload_to='images/order_proof',default ='common/placeholder.png')
    amount = models.FloatField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS, default='pending') 
    request_date_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        return self.user.phone
    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(CashbackRequest, self).save(*args, **kwargs)

    
class WithdrawlRequest(models.Model):
    user = models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS, default='pending') 
    request_date_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        return self.user.phone
    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(WithdrawlRequest, self).save(*args, **kwargs)

@receiver(pre_save, sender=WithdrawlRequest)
def update_wallet_balance(sender, instance, **kwargs):
    try:
        old_instance = WithdrawlRequest.objects.get(id=instance.id)
    except WithdrawlRequest.DoesNotExist:
        user_transaction = UserWalletTransaction(user=instance.user,transaction_type='debited',amount=instance.amount,paid_for='Withdrawl Requested')
        user_transaction.save()
        return None      
            
    if old_instance.status == 'approved' and instance.status == 'pending':
        instance.status = 'approved'
        