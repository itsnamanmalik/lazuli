from django.shortcuts import render
from django.views import View
from website.models import *
from api.affiliate.models import *
from api.ui.models import *
from api.common.models import *
from django.contrib import messages
from django.shortcuts import redirect
from api.users.models import User, UserWalletTransaction
from api.vendors.models import VendorSale
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from api.cron import credit_cashback, create_withdrawl_request

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

        context = {'otp_sent':False,'phone':''}
        return render(request,'login.html',context)
    def post(self, request):
        try:
            request.session['phone']
            return redirect('account')
        except KeyError:
            pass
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
                querystring = {
                    "authorization":"RU8HVru1LvMt0xF4hKcgIZdNa6pBEOo3y9DXfze2GTA5WisCQSAvBUTxErYfXgnoiumcOQFwRtJ5W2Ms",
                    "sender_id":"TXTIND",
                    "message":"Your Lazuli Verification Code is: "+OTP_SENT,
                    "language":"english",
                    "flash":"0",
                    "route":"v3",
                    "numbers":c_phone
                    }
                headers = {
                    'cache-control': "no-cache"
                }
                fire_and_forget(url="https://www.fast2sms.com/dev/bulkV2", headers=headers, querystring=querystring)
                request.session['otp:'+str(c_phone)] = OTP_SENT
                context = {'otp_sent':True,'phone':c_phone}
                messages.success(request,"OTP Sent on your phone!!")
                return render(request,'login.html',context)
        elif otp_p1 and otp_p2 and otp_p3 and otp_p4 and otp_p5 and otp_p6 and c_phone:      
            otp = str(otp_p1)+str(otp_p2)+str(otp_p3)+str(otp_p4)+str(otp_p5)+str(otp_p6)
            try:
                otp_sent = request.session['otp:'+str(c_phone)]
                if otp_sent == otp:
                    try:
                        user = User.objects.get(phone=str(c_phone))
                    except User.DoesNotExist:
                        User.objects.create(phone=str(c_phone))
                        user = User.objects.get(phone=str(c_phone))
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


class Account(View):
    def get(self, request):
        try:
            phone = request.session['phone']
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                del request.session['phone']
                return redirect('login')       
        except KeyError:
            return redirect('login')

        all_transactions = UserWalletTransaction.objects.filter(user=user).order_by('-time_date')
        all_purchase = VendorSale.objects.filter(user=user).order_by('-date_created')
        context = {'user':user,"all_transactions":all_transactions,"all_purchase":all_purchase}
        return render(request,'account.html',context)
    def post(self, request):
        logout = request.POST.get('logout','false')
        address = request.POST.get('address')
        name = request.POST.get('name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('dob')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        
        if logout == 'true':
            try:
                del request.session['phone']
            except KeyError:
                pass
            messages.success(request,"Logedout Successfully!!")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        elif address:
            messages.success(request,"Address Added Successfully!!")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    

        elif name and email:
            try:
                phone = request.session['phone']
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    del request.session['phone']
                    return redirect('login')       
            except KeyError:
                return redirect('login')
            if name:
                user.name = name
            if email:
                user.email = email
            if date_of_birth:
                user.date_of_birth = date_of_birth
            if account_number:
                user.account_number = account_number
            if ifsc_code:
                user.ifsc_code = ifsc_code
            user.save()
            messages.success(request,"User Profile Updated!!")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    
        messages.error(request,"Invalid Request!!")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        


class DeployCashback(View):
    def get(self, request):
        if request.user:
            if request.user.is_superuser:
                credit_cashback()
                messages.success(request,"Cashback credited!!")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
class WithdrawCashback(View):
    def get(self, request):
        if request.user:
            if request.user.is_superuser:
                create_withdrawl_request()
                messages.success(request,"Withdrawl request created!!")
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
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
    
       
            
class Categories(View):
    def get(self, request):
        all_categories = DealsCoupon.objects.all()
        count = all_categories.count()
        context = {"all_categories": all_categories,"count": count}
        return render(request,'all-categories.html',context)
    
       
        
class Stores(View):
    def get(self, request):
        all_stores = Store.objects.all()
        count = all_stores.count()
        context = {"all_stores": all_stores,"count": count}
        return render(request,'all-stores.html',context)
    
    
    
    