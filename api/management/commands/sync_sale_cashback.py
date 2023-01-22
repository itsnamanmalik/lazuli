from django.core.management.base import BaseCommand
from api.users.models import *
from api.vendors.models import VendorSale
from django.db import IntegrityError

class Command(BaseCommand):
    def handle(self, *args, **options):    
        all_cashback = UserCashbackLevel.objects.all()
        for cashback in all_cashback:
            cashback.save()
            print("Cashback Synced!!! "+str(cashback))

