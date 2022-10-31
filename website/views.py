from django.shortcuts import render
from django.views import View
from website.models import *
from api.affiliate.models import *
from api.ui.models import *
from api.common.models import *
from django.contrib import messages
from django.shortcuts import redirect
from api.users.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from api.cron import credit_cashback

import random
import string
import requests

import threading

def request_task(url,headers,querystring):
    requests.get(url, headers=headers, params=querystring)


def fire_and_forget(url,headers,querystring):
    threading.Thread(target=request_task, args=(url, headers,querystring)).start()

def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string

class Login(View):
    def get(self, request):
        try:
            request.session['phone']
            return redirect('account')
        except KeyError:
            pass
        all_city = City.objects.all()
        try:
            location = request.session['city'] +' - '+request.session['pincode']
        except KeyError:
            location = 'Location'
        context = {'all_city':all_city,'location':location,'otp_sent':False,'phone':''}
        return render(request,'login.html',context)
    def post(self, request):
        try:
            request.session['phone']
            return redirect('account')
        except KeyError:
            pass
        all_city = City.objects.all()
        try:
            location = request.session['city'] +' - '+request.session['pincode']
        except KeyError:
            location = 'Location'
        c_phone = request.POST.get('phone')
        otp_p1 = request.POST.get('otp_p1')
        otp_p2 = request.POST.get('otp_p2')
        otp_p3 = request.POST.get('otp_p3')
        otp_p4 = request.POST.get('otp_p4')
        otp_p5 = request.POST.get('otp_p5')
        otp_p6 = request.POST.get('otp_p6')
        if c_phone and not otp_p1 and not otp_p2 and not otp_p3 and not otp_p4 and not otp_p5 and not otp_p6:
            if len(c_phone) == 10 and c_phone.isnumeric():
                OTP_SENT = get_random_alphanumeric_string(0,6)
                querystring = {"authorization":"RU8HVru1LvMt0xF4hKcgIZdNa6pBEOo3y9DXfze2GTA5WisCQSAvBUTxErYfXgnoiumcOQFwRtJ5W2Ms","sender_id":"TXTIND","message":"Your Get Fixed Verification Code is: "+OTP_SENT,"language":"english","flash":"0","route":"v3","numbers":c_phone}
                headers = {
                    'cache-control': "no-cache"
                }
                fire_and_forget(url="https://www.fast2sms.com/dev/bulkV2", headers=headers, querystring=querystring)
                request.session['otp:'+str(c_phone)] = OTP_SENT
                context = {'all_city':all_city,'location':location,'otp_sent':True,'phone':c_phone}
                messages.success(request,"OTP Sent on your phone!!")
                return render(request,'login.html',context)
        elif otp_p1 and otp_p2 and otp_p3 and otp_p4 and otp_p5 and otp_p6 and c_phone:      
            otp = str(otp_p1)+str(otp_p2)+str(otp_p3)+str(otp_p4)+str(otp_p5)+str(otp_p6)
            try:
                otp_sent = request.session['otp:'+str(c_phone)]
                if otp_sent == otp:
                    try:
                        user = User.objects.get(phone='+91'+str(c_phone))
                    except User.DoesNotExist:
                        User.objects.create(phone='+91'+str(c_phone),user_id=get_random_alphanumeric_string(3,3))
                        user = User.objects.get(phone='+91'+str(c_phone))
                    request.session['phone'] = str(user.phone)
                    messages.success(request,"Logedin Successfully!!")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                else:
                    try:
                        del request.session['phone']
                    except KeyError:
                        pass
                    messages.error(request,"Invalid OTP!!")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            except KeyError:
                messages.error(request,"Invalid OTP!!")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class DeployCashback(View):
    def get(self, request):
        credit_cashback()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



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
    
    
    
    