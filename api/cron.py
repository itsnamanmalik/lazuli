from django.db.models import F
from django.db import IntegrityError
from api.users.models import UserCashbackLevel, UserWalletTransaction
from api.vendors.models import VendorSale
from api.cashback.models import CashbackLevel
from django.db.models import Sum



#percent calc
def credit_cashback():
    total_revenue = VendorSale.objects.filter(cashback_credited=False).aggregate(Sum('total_amount'))['total_amount__sum']
    total_cashback = (total_revenue*50)/100
    all_cashback_levels = CashbackLevel.objects.all()
    for cashback_level in all_cashback_levels:
        level_cashback = (total_cashback*cashback_level.percentage)/100
        equal_cashback = (level_cashback*cashback_level.fixed_distribution_percentage)/100
        ratio_cashback = (level_cashback*cashback_level.ratio_distribution_percentage)/100
        this_level_users_cashback = UserCashbackLevel.objects.filter(cashback_level=cashback_level)
        total_level_revenue = this_level_users_cashback.aggregate(Sum('sale__total_amount'))['sale__total_amount__sum']
        total_level_count = this_level_users_cashback.count()
        for level_user_cashback in this_level_users_cashback:
            this_ratio_cashback = ((level_user_cashback.sale.total_amount/total_level_revenue)*ratio_cashback)
            this_equal_cashback = equal_cashback/total_level_count
            single_cashback_amount = this_equal_cashback+this_ratio_cashback
            if single_cashback_amount > ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100):
                single_cashback_amount = ((level_user_cashback.sale.total_amount*level_user_cashback.cashback_level.percentage)/100)
            user_transaction = UserWalletTransaction(user=level_user_cashback.user,transaction_type='',amount=(this_equal_cashback+this_ratio_cashback),paid_for='Cashback For Purchase')
            user_transaction.save()
