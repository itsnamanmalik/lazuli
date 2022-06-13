from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from api.users.models import User
from api.vendors.models import Vendor, VendorSale,VedorCommissionsTransaction
from django.db.models import Sum

class Dashboard(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        
        allsales = VendorSale.objects.filter(vendor=vendor)
        salecount = allsales.count()
        if salecount>0:
            saletotal = allsales.aggregate(Sum('total_amount'))['total_amount__sum']
        else:
            saletotal = 0
        total_users = User.objects.all().count()
        total_sum = allsales.filter(marketing_fee_paid=False).aggregate(Sum('total_amount'))['total_amount__sum']
        if total_sum:
            marketing_fee_pending = ((total_sum)*vendor.commission_percentage)/100
        else:
            marketing_fee_pending = 0
        context = {'vendor': vendor,'saletotal':saletotal,'salecount':salecount,'total_users':total_users,'marketing_fee_pending':marketing_fee_pending}    
        return render(request,'vendor/dashboard.html',context)
    
        
class VendorLogin(View):
    def get(self, request):
        try:
            request.session['phone']
            return redirect('dashboard')
        except KeyError:
            pass
        return render(request,'vendor/login.html')
    
    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if phone and password:
            try:
                vendor = Vendor.objects.get(phone=phone, password=password)
                request.session['phone'] = str(vendor.phone)
            except Vendor.DoesNotExist:
                messages.error(request,"Invalid Credentials!!")    
            messages.success(request,"Logedin Successfully!!")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
        
class Sales(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')  
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        
        allsales = VendorSale.objects.filter(vendor=vendor)
        context = {'vendor': vendor,"allsales":allsales}    
        return render(request,'vendor/sales.html',context)

        
class MarketingFee(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')  
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        allsales = VendorSale.objects.filter(vendor=vendor)
        total_ammount = allsales.filter(marketing_fee_paid=False).aggregate(Sum('total_amount'))['total_amount__sum']
        if total_ammount:
            marketing_fee_pending = ((total_ammount)*vendor.commission_percentage)/100
        else:
            marketing_fee_pending = 0 
        alltransaction = VedorCommissionsTransaction.objects.filter(vendor=vendor)
        context = {'vendor': vendor,"alltransaction":alltransaction,"marketing_fee_pending":marketing_fee_pending}    
        return render(request,'vendor/marketing.html',context)
    


        
        
class MyProfile(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        
        
        context = {'vendor': vendor}    
        return render(request,'vendor/my-profile.html',context)
    
    def post(self, request):
        name = request.POST.get('name')
        business_name = request.POST.get('business-name')
        business_type = request.POST.get('business-type')
        email = request.POST.get('email')
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        
        vendor.name = name
        vendor.business_name = business_name
        vendor.business_type = business_type
        vendor.email = email
        vendor.save()
                
        messages.success(request,"Profile updated Successfully!!")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
        
class ResetPassword(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
        context = {'vendor': vendor}    
        return render(request,'vendor/reset-pass.html',context)
    
    def post(self, request):
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')
        if current_password and new_password and confirm_password:
            try:
                phone = request.session['phone']
            except KeyError:
                return redirect('vendor-login')
            try:
                vendor = Vendor.objects.get(phone=phone)
            except Vendor.DoesNotExist:
                return redirect('vendor-logout')
            if vendor.password != current_password:
                messages.error(request,"Invalid Password!!")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            if new_password != confirm_password:
                messages.error(request,"New Password and Confirm Password do not match!!")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            vendor.password = new_password
            vendor.save()
            messages.success(request,"Password reset successfully!")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                
        
        
    
        
class AddSales(View):
    def get(self, request):
        try:
            phone = request.session['phone']
        except KeyError:
            return redirect('vendor-login')
        try:
            vendor = Vendor.objects.get(phone=phone)
        except Vendor.DoesNotExist:
            return redirect('vendor-logout')
                
        context = {'vendor': vendor}    
        return render(request,'vendor/add-sales.html',context)
    
    
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_phone = request.POST.get('phone')
        product_name = request.POST.get('product-name')
        amount = request.POST.get('amount')
        
        if name and user_phone and product_name and amount:
            amount = float(amount)
            try:
                phone = request.session['phone']
            except KeyError:
                return redirect('vendor-login')
            try:
                vendor = Vendor.objects.get(phone=phone)
            except Vendor.DoesNotExist:
                return redirect('vendor-logout')
            
            try:
                user = User.objects.get(phone=user_phone)
            except User.DoesNotExist:
                user = User(phone=user_phone, name=name, email=email)
                user.save()
            vendor_sales = VendorSale(user=user, vendor=vendor,product_name=product_name,total_amount=amount)
            vendor_sales.save()
                    
            messages.success(request,"Sales Added Successfully!!")
            return redirect('sales')
        messages.error(request,"Some error occured!!")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    
    
class Logout(View):
    def get(self, request):
        try:
            del request.session['phone']
        except KeyError:
            pass
        messages.success(request,"Logedout Successfully!!")
        return redirect('vendor-login')