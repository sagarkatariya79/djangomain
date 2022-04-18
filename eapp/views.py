from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login as auth_login
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.
def index(request):
    recent_products = Products.objects.all().order_by('-id')[:6]
    customer_review = Contact.objects.all().order_by('-id')[:2]
    try:
        user= User.objects.get(email=request.session['email'])
        carts=Cart.objects.filter(user=user,status=False)
        final_price=0
        for i in carts:
            final_price=i.total_price+final_price
        return render(request,'index.html',{'recent_products':recent_products,'carts':carts,'customer_review':customer_review,'final_price':final_price})
    except:
        return render(request,'index.html',{'recent_products':recent_products,'customer_review':customer_review})

#Contact us page logic
def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name = request.POST["name"],
            email = request.POST["email"],
            message = request.POST["message"]

        )
        msg = "*Message Sent Sucessfully*"
        return render(request, 'contact.html', { 'msg' : msg } )
    else:
        try:
            user = User.objects.get(email=request.session['email'])
            carts = Cart.objects.filter(user=user,status=False)
            final_price = 0
            for i in carts:
                final_price = i.total_price + final_price
            return render(request,'contact.html',{'carts':carts,'final_price':final_price})

        except:
            return render(request, 'contact.html')





def about(request):
    return render(request,'about.html')


def underconstruction(request):
    return render(request,'under-construction.html')


def signup(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["cpassword"]:
            
            User.objects.create(
            fname = request.POST["fname"],
            lname = request.POST["lname"],
            email = request.POST["email"],
            mobile = request.POST["mobile"],
            address=request.POST['address'],
            password = request.POST["password"],
            image = request.FILES["image"],
            usertype = request.POST['usertype'],
            )
            msg = "Signup Sucessfully"
            return render(request,'signup.html',{"msg" : msg})
        else:
            msg = "Password Doesnot match"
            return render(request,'signup.html',{"msg" : msg })
    else:
        return render(request,'signup.html')



def signin(request):
    if request.method == 'POST':
        try:
            uservar = User.objects.get(
                email = request.POST['email'],
                password = request.POST['password']
                )
            if uservar.usertype == 'user':
                request.session['email'] = uservar.email
                request.session['fname'] = uservar.fname
                request.session['image'] = uservar.image.url
                recent_products = Products.objects.all().order_by('-id')[:6]
                customer_review = Contact.objects.all().order_by('-id')[:2]
                wishlist = Wishlist.objects.filter(user=uservar)
                request.session['wishlist_count'] =len(wishlist)
                carts= Cart.objects.filter(user=uservar,status=False)
                cart= Cart.objects.filter(user=uservar,status=False)
                request.session['cart_count']= len(cart)
                final_price = 0
                for i in carts:
                    final_price = i.total_price + final_price
                return render(request,'index.html',{'recent_products':recent_products,'carts':carts,'customer_review':customer_review,'final_price':final_price})

            elif uservar.usertype == 'seller':
                request.session['email'] = uservar.email
                request.session['fname'] = uservar.fname
                request.session['image'] = uservar.image.url
                products=Products.objects.filter(product_seller=uservar).order_by('-id')[:6]
                return render(request,'sellerindex.html',{'products':products})

        except Exception as e:
            print('---------',e)
            msg= "*Invalid Username or Password*"
            return render(request,'signin.html',{"msg" : msg})

    else:
        return render(request,'signin.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['image']
        del request.session['wishlist_count']
        del request.session['cart_count']
        return render(request,'signin.html')


            
    except:
        return render(request,'signin.html')

def changepassword(request):
    if request.method =='POST':

        uservar = User.objects.get(
            email = request.session['email']
            )

        if uservar.password == request.POST['old_password']:
        
            if request.POST['new_password'] == request.POST['cnew_password']:
                uservar.password = request.POST['new_password']
                uservar.save()
                return redirect('logout')
            else:
                msg ="New password & Confirm new password Does not match"
                return render(request,'changepassword.html',{'msg' : msg})
        
        else:
            msg = "Old password Doesnot match"
            return render(request,'changepassword.html',{'msg':msg})
    else:
        return render(request,'changepassword.html')



def forgotpassword(request):
    if request.method == 'POST':

        try:
            uservar = User.objects.get(email = request.POST['email'])
            email = uservar.email
            otp = random.randint(100000,999999)
            subject = 'Django Password Reset'
            message = f'Hi {uservar.fname},Your OTP for django website is {otp},Thank You.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [uservar.email, ]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,'otppage.html',{'email':email,"otp" :otp})

        except Exception as e:
            print("-------------",e) 
            msg = "Email is not registered"
            return render(request,'forgotpassword.html',{'msg':msg})
    else:
        return render(request,'forgotpassword.html')


def otppage(request):
    email = request.POST['email']
    otp = request.POST['otp']
    userotp = request.POST['userotp']

    if otp == userotp :
        return render(request,'newpassword.html',{'email':email})
    else:
        msg = "Please Enter Valid OTP"
        return render(request,'otppage.html',{'otp':otp,'email':email,'msg':msg})


def newpassword(request):
    email = request.POST['email']
    if request.POST['npassword'] == request.POST['cnpassword']:
        uservar = User.objects.get(email= email)
        uservar.password = request.POST['cnpassword']
        uservar.save()
        return redirect('logout')
    else:
        msg = "Password & Confirm Password Doesnot Match"
        return render(request,'newpassword.html',{'msg':msg ,'email':email})


def sellerindex(request):
    user= User.objects.get(email=request.session['email'])
    products=Products.objects.filter(product_seller=user).order_by('-id')[:6]
    return render(request,'sellerindex.html',{'products':products})

def sellerchangepassword(request):
    if request.method =='POST':

        uservar = User.objects.get(
            email = request.session['email']
            )

        if uservar.password == request.POST['old_password']:
        
            if request.POST['new_password'] == request.POST['cnew_password']:
                uservar.password = request.POST['new_password']
                uservar.save()
                return redirect('logout')
            else:
                msg ="New password & Confirm new password Does not match"
                return render(request,'sellerchangepassword.html',{'msg' : msg})
        
        else:
            msg = "Old password Doesnot match"
            return render(request,'sellerchangepassword.html',{'msg':msg})
    else:
        return render(request,'sellerchangepassword.html')

def selleraddproducts(request):
    if request.method == 'POST':
        uservar = User.objects.get(email = request.session['email'])
        Products.objects.create(
        product_seller = uservar,
        product_category = request.POST['product_category'],
        product_company = request.POST['product_company'],
        product_name = request.POST['product_name'],
        product_desc = request.POST['product_desc'],
        product_price = request.POST['product_price'],
        product_image = request.FILES['product_image'],
        )
        msg = "Product Added Sucessfully"
        return render(request,'selleraddproducts.html',{'msg':msg})


    else:
        return render(request,'selleraddproducts.html')




def sellerviewproducts(request):
    seller = User.objects.get(email = request.session['email'])
    products = Products.objects.filter(product_seller= seller)
    return render(request,'sellerviewproducts.html',{'products': products})


def sellereditproducts(request,pk):
    product = Products.objects.get(pk=pk)
    if request.method == "POST":
        product.product_name = request.POST['product_name']
        product.product_desc = request.POST['product_desc']
        product.product_price = request.POST['product_price']
        try:
            product.product_image = request.FILES['product_image']
        except:
            pass
        product.save()
        msg = "Product updated sucessfully"
        return render(request,'sellereditproducts.html',{'product' : product , 'msg':msg})

    else:
        return render(request,'sellereditproducts.html',{'product' : product})

def sellerdeleteproducts(request,pk):
    product = Products.objects.get(pk=pk)
    product.delete()
    return redirect('sellerviewproducts')




def product_filter(request,pc):
    #why
    products = Products()
    user = User.objects.get(email=request.session['email'])
    if pc=="All":
        products = Products.objects.filter(product_seller=user)
    else:
        products = Products.objects.filter(product_seller=user,product_category = pc)
    return render(request,'sellerviewproducts.html',{'products':products})



def product_detail(request,pk):
    try:
        user = User.objects.get(email=request.session['email'])
    except:
        pass
    products = Products.objects.get(pk=pk)
    wishlist_flag =False
    try:
        wishlist = Wishlist.objects.get(user=user,products=products)
        wishlist_flag=True
    except:
        pass

    cart_flag=False
    try:
        cart=Cart.objects.get(user=user,product=products,status=False)
        cart_flag=True
    except:
        pass
    return render(request,'product_detail.html',{'products':products,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})


def add_to_wishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    products = Products.objects.get(pk=pk)
    Wishlist.objects.create(
        user=user,
        products=products,
        )
    return redirect('wishlist')

def remove_from_wishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    products= Products.objects.get(pk=pk)
    wishlist= Wishlist.objects.filter(user=user,products=products)
    wishlist.delete()
    return redirect('wishlist')    

def wishlist(request):
    try:
        user = User.objects.get(email = request.session['email'])
        wishlist = Wishlist.objects.filter(user=user)
        carts = Cart.objects.filter(user=user,status=False)
        request.session['wishlist_count'] =len(wishlist)
        final_price = 0
        for i in carts:
            final_price = i.total_price + final_price
        return render(request,'wishlist.html',{'wishlist':wishlist,'carts':carts,'final_price':final_price})
    except:
        return render(request,'wishlist.html')



def shop(request):
    products = Products.objects.all()
    try:
        user= User.objects.get(email=request.session['email'])
        carts = Cart.objects.filter(user=user,status=False)
        final_price=0
        for i in carts:
            final_price = i.total_price + final_price
        return render(request,'shop.html',{'products':products,'carts':carts,'final_price':final_price})
    except:
        return render(request,'shop.html',{'products':products})

def cart(request):
    try:
        user = User.objects.get(email=request.session['email'])
        carts = Cart.objects.filter(user=user,status=False)
        final_price = 0
        for i in carts:
            final_price = i.total_price + final_price
        request.session['cart_count']= len(carts)

        return render(request,'cart.html',{'carts':carts,'final_price':final_price})
    except:
        return render(request,'cart.html')


def add_to_cart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product=Products.objects.get(pk=pk)
    Cart.objects.create(
        user=user,
        product=product,
        product_price=product.product_price,
        total_price=product.product_price,
        )

    return redirect('cart')




def remove_from_cart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product=Products.objects.get(pk=pk)
    cart=Cart.objects.get(user=user,product=product,status=False)
    cart.delete()
    return redirect('cart')



def checkout(request):
    user=User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user,status=False)
    total_price=0
    for i in cart:
        total_price=i.total_price+total_price

    return render(request,'checkout.html',{'cart':cart,'user':user,'total_price':total_price})


def initiate_payment(request):
    user = User.objects.get(email=request.session['email'])
    cart= Cart.objects.filter(user=user,status=False)
    try:
        amount = int(request.POST['amount'])
    except Exception as e:
        print('++++++++',e)
        return render(request, 'checkout.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    for i in cart:
        i.status=True
        i.save()

    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)



def orders(request):
    user = User.objects.get(email=request.session['email'])
    cartorder= Cart.objects.filter(user=user,status=True)
    carts = Cart.objects.filter(user=user,status=False)
    return render(request,'orders.html',{'cartorder':cartorder,'carts':carts})

def cancel_order(request,pk):
    user= User.objects.get(email=request.session['email'])
    product =Products.objects.get(pk=pk)
    cartorder =Cart.objects.get(product=product,user=user)
    cartorder.status=False
    cartorder.save
    return redirect('orders')



def user_product_filter(request,pc):
    if pc == 'All':
        products = Products.objects.all()
    else:
        products = Products.objects.filter(product_category=pc)
    return render(request,'shop.html',{'products':products})



def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def search(request):
    products =Products
    search= request.POST['search']
    products= Products.objects.filter(product_category__contains=search)
    return render(request,'shop.html',{'products':products})