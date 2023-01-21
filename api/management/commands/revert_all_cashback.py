from django.core.management.base import BaseCommand
from api.users.models import *
from api.vendors.models import VendorSale
from django.db import IntegrityError

class Command(BaseCommand):
    def handle(self, *args, **options):    
        UserWalletTransaction.objects.all().delete()
        User.objects.all().update(wallet=0)
        VendorSale.objects.all().update(cashback_credited_once=False,cashback_given=0,full_cashback_credited=False)
        print("All Cashback reverted!!!")