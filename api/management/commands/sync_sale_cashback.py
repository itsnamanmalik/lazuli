from django.core.management.base import BaseCommand
from api.users.models import *
from api.vendors.models import VendorSale
from django.db import IntegrityError
from django.db.models import Sum

class Command(BaseCommand):
    def handle(self, *args, **options):    
        all_sale = VendorSale.objects.all()
        for sale in all_sale:
            amount_paid = UserWalletTransaction.objects.filter(cashback_level__sale=sale,transaction_type='credited').aggregate(Sum('amount'))['amount__sum']
            if amount_paid:
                sale.cashback_given = amount_paid
                sale.save()
            print("Sale cashback Synced!!! "+str(sale))

