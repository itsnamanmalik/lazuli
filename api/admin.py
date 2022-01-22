from django.contrib import admin

from api.ui.models import *
from api.common.models import *
from api.affiliate.models import *
from api.users.models import *
from api.vendors.models import *
from api.customer_requests.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as StaffUser
from api.models import CustomUser
from rest_framework.authtoken.models import TokenProxy
from django.utils.html import format_html
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

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','wallet','date_joined','last_login')
    search_fields = ('name','email','phone',)
    list_filter = ('date_of_birth',)


@admin.register(UserWalletTransaction)
class UserWalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('user','transaction_type','amount')
    list_filter = ('transaction_type',)
        

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
    

@admin.register(VendorSale)
class VendorSaleAdmin(admin.ModelAdmin):
    list_display = ('vendor','user')
    list_filter = ('vendor','user',)
    filter_input_length = {
        "user": 6,
    }
    

