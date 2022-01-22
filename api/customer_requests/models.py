from django.db import models



STATUS = (
    ("pending", "pending"), 
    ("approved", "approved"), 
)


class CashbackRequest(models.Model):
    user = models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    order_proof = models.ImageField(upload_to='images/order_proof',default ='common/placeholder.png')
    status = models.CharField(max_length=10, choices=STATUS, default='pending') 
    request_date_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        return self.user.phone

    
class WithdrawlRequest(models.Model):
    user = models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS, default='pending') 
    request_date_time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        return self.user.phone

