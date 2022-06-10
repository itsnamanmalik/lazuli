from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect


class Dashboard(View):
    def get(self, request):
        return render(request,'vendor/dashboard.html')
    
        
class VendorLogin(View):
    def get(self, request):
        return render(request,'vendor/login.html')
    
        
class Sales(View):
    def get(self, request):
        return render(request,'vendor/sales.html')
    
        
class MyProfile(View):
    def get(self, request):
        return render(request,'vendor/my-profile.html')
    
        
class ResetPassword(View):
    def get(self, request):
        return render(request,'vendor/reset-pass.html')
    
        
class AddSales(View):
    def get(self, request):
        return render(request,'vendor/add-sales.html')
    
    