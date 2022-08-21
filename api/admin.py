from django.contrib import admin
from api.ui.models import *
from api.common.models import *
from api.affiliate.models import *
from api.users.models import *
from api.vendors.models import *
from api.customer_requests.models import *
from api.cashback.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as StaffUser
from api.models import CustomUser
from rest_framework.authtoken.models import TokenProxy
from import_export.admin import ExportMixin
from import_export import resources
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ExportMixin
from import_export import resources

admin.site.site_header='Lazuli'
admin.site.site_title = 'Lazuli'

admin.site.unregister(TokenProxy)
admin.site.unregister(StaffUser)
admin.site.register(CustomUser, UserAdmin)


admin.site.register(SliderLocation)
admin.site.register(Slider)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent_category')

admin.site.register(Brand)


class UserCashbackLevelAdmin(admin.StackedInline):
    model = UserCashbackLevel    

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserCashbackLevelAdmin]
    list_display = ('name','email','phone','wallet','date_joined','last_login')
    search_fields = ('name','email','phone',)
    list_filter = ('date_of_birth',)



class TransactionResource(resources.ModelResource):
    class Meta:
        model = UserWalletTransaction
        fields = ('user__phone','transaction_type','amount','paid_for','transaction_breakdown','time_date')


@admin.register(UserWalletTransaction)
class UserWalletTransactionAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = TransactionResource
    list_display = ('user','transaction_type','amount','time_date')
    list_filter = ('transaction_type','is_cashback_transaction','time_date')
    # def get_date(self,obj):
    #     if obj.time_date:
    #         return obj.time_date
        # ,('time_date', DateRangeFilter)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name','cashback_percent','cashback_type')
    
    
@admin.register(DealsCoupon)
class DealsCouponAdmin(admin.ModelAdmin):
    list_display = ('title','store','coupon_code')
    list_filter = ('store',)
    

class ProductPriceAdmin(admin.StackedInline):
    model = ProductPrice

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','category','brand')
    inlines = [ProductPriceAdmin, ProductImageAdmin]


@admin.register(CashbackRequest)
class CashbackRequestAdmin(admin.ModelAdmin):
    list_display = ('user','status','request_date_time')
    

@admin.register(WithdrawlRequest)
class WithdrawlRequestAdmin(admin.ModelAdmin):
    list_display = ('user','amount','status','request_date_time')
    

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name','business_name','phone')
    

@admin.register(VedorCommissionsTransaction)
class VedorCommissionsTransactionAdmin(admin.ModelAdmin):
    list_display = ('vendor','total_amount','payment_status','date_created','last_edited')
    list_filter = ('vendor','payment_status',)
    

@admin.register(VendorSale)
class VendorSaleAdmin(admin.ModelAdmin):
    list_display = ('vendor','user','product_name','total_amount','after_sale_total','marketing_fee_paid','date_created','last_edited')
    list_filter = ('vendor','user',)   

@admin.register(CashbackLevel)
class CashbackLevelAdmin(admin.ModelAdmin):
    list_display = ('name','percentage','fixed_distribution_percentage','ratio_distribution_percentage')
    search_fields = ('name',)


@admin.register(UserCashbackLevel)
class UserCashbackLevelAdmin(admin.ModelAdmin):
    list_display = ('user','sale','cashback_level','given_cashback')
    
