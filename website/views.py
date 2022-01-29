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
    
    
    
    