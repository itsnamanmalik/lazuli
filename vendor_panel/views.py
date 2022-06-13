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