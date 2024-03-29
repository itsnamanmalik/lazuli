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

admin.site.site_header='Lazuli'
admin.site.site_title = 'Lazuli'

admin.site.unregister(TokenProxy)
admin.site.unregister(StaffUser)
admin.site.register(CustomUser, UserAdmin)


admin.site.register(SliderLocation)
admin.site.register(Slider)

admin.site.register(TransactionError)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent_category')

admin.site.register(Brand)

def mark_status_approved(self, request, queryset):
    for obj in queryset:
        obj.status = 'approved'
        obj.save()
def mark_status_cancelled(self, request, queryset):
    for obj in queryset:
        obj.status = 'cancelled'
        obj.save()

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
    
class WithdrawlRequestAdminResource(resources.ModelResource):
    class Meta:
        model = WithdrawlRequest
        fields = ('user__name','user__account_number','user__bank_name','user__email','user__ifsc_code','amount','request_date_time',)


@admin.register(WithdrawlRequest)
class WithdrawlRequestAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = WithdrawlRequestAdminResource
    list_display = ('user','amount','status','request_date_time')
    actions = [mark_status_approved,mark_status_cancelled]
    list_filter = ('status',)
    

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name','business_name','phone','marketing_fee_pending')

    def marketing_fee_pending(self, obj):
        all_pending_sale = VendorSale.objects.filter(vendor=obj,marketing_fee_paid=False)
        maketing = 0
        for pending_sale in all_pending_sale:
            maketing = maketing + ((pending_sale.total_amount * pending_sale.commision_percentage)/100)
        return maketing
    

@admin.register(VedorCommissionsTransaction)
class VedorCommissionsTransactionAdmin(admin.ModelAdmin):
    list_display = ('vendor','total_amount','payment_status','date_created','last_edited')
    list_filter = ('vendor','payment_status',)

class VendorSaleAdminResource(resources.ModelResource):
    class Meta:
        model = VendorSale
        fields = ('vendor__name','user__name','product_name','total_amount','after_sale_total','marketing_fee_paid','cashback_given','date_created','last_edited',)

@admin.register(VendorSale)
class VendorSaleAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = VendorSaleAdminResource
    search_fields = ('product_name',)
    list_display = ('vendor','user','product_name','total_amount','after_sale_total','marketing_fee_paid','date_created','last_edited')
    list_filter = ('vendor','user',)   

@admin.register(CashbackLevel)
class CashbackLevelAdmin(admin.ModelAdmin):
    list_display = ('name','percentage','fixed_distribution_percentage','ratio_distribution_percentage')
    search_fields = ('name',)


@admin.register(UserCashbackLevel)
class UserCashbackLevelAdmin(admin.ModelAdmin):
    list_display = ('user','sale','cashback_level','given_cashback')
    
