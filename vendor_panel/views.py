from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from api.vendors.models import Vendor


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
        
        
        context = {'vendor': vendor}    
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
        
        
        context = {'vendor': vendor}    
        return render(request,'vendor/sales.html',context)
    
        
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
    
    
class Logout(View):
    def get(self, request):
        try:
            del request.session['phone']
        except KeyError:
            pass
        messages.success(request,"Logedout Successfully!!")
        return redirect('vendor-login')