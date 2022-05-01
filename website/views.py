from django.shortcuts import render
from django.views import View
from website.models import *
from api.affiliate.models import *
from api.ui.models import *
from api.common.models import *
from django.contrib import messages
from django.shortcuts import redirect

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse





class Index(View):
    def get(self, request):
        home_sliders = Slider.objects.filter(slider_location__name = "main-home")
        top_categories = Category.objects.all()[:10]
        top_brands = Brand.objects.all()[:10]
        top_deals = DealsCoupon.objects.all()[:10]
        top_stores = Store.objects.all()[:10]
        context = {"home_sliders": home_sliders,"top_categories": top_categories,"top_brands": top_brands,"top_deals": top_deals,"top_stores": top_stores}
        return render(request,'index.html',context)
    
    
class Brands(View):
    def get(self, request):
        all_brands = Brand.objects.all()
        count = all_brands.count()
        context = {"all_brands": all_brands,"count": count}
        return render(request,'all-brands.html',context)
    
    
class Deals(View):
    def get(self, request):
        all_deals = DealsCoupon.objects.all()
        count = all_deals.count()
        context = {"all_deals": all_deals,"count": count}
        return render(request,'all-deals.html',context)
    
       
        
class Stores(View):
    def get(self, request):
        all_stores = Store.objects.all()
        count = all_stores.count()
        context = {"all_stores": all_stores,"count": count}
        return render(request,'all-stores.html',context)
    
    
    
    