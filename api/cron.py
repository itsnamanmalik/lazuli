from django.db.models import F
from django.db import IntegrityError
from api.users.models import UserCashbackLevel, UserWalletTransaction
from api.vendors.models import VendorSale
from api.cashback.models import CashbackLevel,CashbackCreditError
from django.db.models import Sum
from django.db import transaction

#percent calc
def credit_cashback():
    try:
        with transaction.atomic():
            all_vendors_for_cashback = VendorSale.objects.filter(cashback_credited_once=False)
            total_revenue = all_vendors_for_cashback.aggregate(Sum('total_amount'))['total_amount__sum']
            total_profit = 0
            for vendor_cash in all_vendors_for_cashback:
                total_profit = total_profit + ((vendor_cash.total_amount*vendor_cash.vendor.commission_percentage)/100)
            total_cashback = (total_profit*50)/100
            breakdown_init = "Total Revenue: "+str(total_revenue)+"\nTotal Profit: "+str(total_profit)+"\nTotal Cashback We can Distribute: "+str(total_cashback)
            all_cashback_levels = CashbackLevel.objects.all()
            for cashback_level in all_cashback_levels:
                level_cashback = (total_cashback*cashback_level.percentage)/100
                equal_cashback = (level_cashback*cashback_level.fixed_distribution_percentage)/100
                ratio_cashback = (level_cashback*cashback_level.ratio_distribution_percentage)/100
                this_level_users_cashback = UserCashbackLevel.objects.filter(cashback_level=cashback_level,cashback_given=False)
                total_level_revenue = this_level_users_cashback.aggregate(Sum('sale__total_amount'))['sale__total_amount__sum']
                total_level_count = this_level_users_cashback.count()
                
                breakdown_init = breakdown_init+"\n"+str(cashback_level.name)+"Level Cashback: "+str(level_cashback)+"\nEqual Distribution Cashback: "+str(equal_cashback)+"\nRatio Distribution Cashback: "+str(ratio_cashback)+"\n"+str(cashback_level.name)+" Level Cashback Total Revenue: "+str(total_level_revenue)+"\n"+str(cashback_level.name)+" Level Cashback Total Users: "+str(total_level_count)
                
                for level_user_cashback in this_level_users_cashback:
                    this_ratio_cashback = ((level_user_cashback.sale.total_amount/total_level_revenue)*ratio_cashback)
                    this_equal_cashback = equal_cashback/total_level_count
                    single_cashback_amount = this_equal_cashback+this_ratio_cashback
                    breakdown_last = "This Sale Equal Distributed Cashback: "+str(this_equal_cashback)+"\nThis Sale Ratio Distributed Cashback: "+str(this_ratio_cashback)+"\nTotal Cashback: "+str(single_cashback_amount)
                    if single_cashback_amount > ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100):
                        single_cashback_amount = ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100)
                        level_user_cashback.cashback_given = True
                        level_user_cashback.save()
                    level_user_cashback.given_cashback = level_user_cashback.given_cashback + single_cashback_amount
                    level_user_cashback.save()
                    if level_user_cashback.given_cashback > ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100):
                        single_cashback_amount = ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100) - (level_user_cashback.given_cashback - single_cashback_amount)
                        level_user_cashback.given_cashback = ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100)
                        level_user_cashback.cashback_given = True
                        level_user_cashback.save()
                    breakdown_last = breakdown_last+"\nAfter checking if Total cashback for this sale is greater than sale amount or level percent of sale amount: "+str(single_cashback_amount)
                    final_breakdown = breakdown_init+"\n\n"+breakdown_last
                    user_transaction = UserWalletTransaction(user=level_user_cashback.user,transaction_type='credited',cashback_level=level_user_cashback,amount=(single_cashback_amount),paid_for='Cashback For Purchase',transaction_breakdown=final_breakdown)
                    user_transaction.save()
            VendorSale.objects.filter(cashback_credited_once=False).update(cashback_credited_once=True)
    except Exception as ex:
        CashbackCreditError.objects.create(exception_message=str(ex))
        
