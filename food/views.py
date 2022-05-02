from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')
    # return render(request,'index.html')

#for showing signup/login button for NGO
def ngoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'ngoclick.html')

#for showing signup/login button for Donar
def donarclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'donarclick.html')

def ngo_signup_view(request):
    form1=forms.NGOUserForm()
    form2=forms.NGOExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.NGOUserForm(request.POST)
        form2=forms.NGOExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_ngo_group = Group.objects.get_or_create(name='NGO')
            my_ngo_group[0].user_set.add(user)

        return HttpResponseRedirect('ngologin')
    return render(request,'ngosignup.html',context=mydict)

def donar_signup_view(request):
    form1=forms.DonarUserForm()
    form2=forms.DonarExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.DonarUserForm(request.POST)
        form2=forms.DonarExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_donar_group = Group.objects.get_or_create(name='DONAR')
            my_donar_group[0].user_set.add(user)

        return HttpResponseRedirect('donarlogin')
    return render(request,'donarsignup.html',context=mydict)

#for checking user is NGO or Donar
def is_ngo(user):
    return user.groups.filter(name='NGO').exists()
def is_donar(user):
    return user.groups.filter(name='DONAR').exists()

def afterlogin_view(request):
    if is_ngo(request.user):
        return redirect('ngo-dashboard')
    elif is_donar(request.user):
        return redirect('donar-dashboard')

#for NGO LOGIN SECTION
@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_dashboard_view(request):
    ngodata=models.NGOExtra.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'address':ngodata[0].address,
        'mobile':ngodata[0].mobile,
        'date':ngodata[0].joindate,
        'notice':notice
    }
    return render(request,'ngo_dashboard.html',context=mydict)

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_donation_view(request):
    donations = models.Donation.objects.all()
    claimed=models.NGOExtra.objects.all().filter(user_id=request.user.id)

    context = {'donations':donations, 'id':claimed[0].id}
    return render(request,'ngo_donation.html', context)

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def claim_donation_view(request, pk1, pk2, pk3):
    # print(don.status)
    don = models.Donation.objects.get(id=pk1)
    ngo = models.NGOExtra.objects.get(id=pk2)
    cla = models.Claim()
    # print(don.status)
    # if request.method == "POST":
    cla.ngoname=request.user.first_name
    cla.foodName=pk3
    cla.mobile=ngo.mobile
    cla.address=ngo.address    

    don.status=True
    # ngo.claimed=True

    don.save()
    ngo.save()
    cla.save()
    messages.success(request, "Claimed Successfully!!")
    # return render(request,'student-attendance')
    return redirect(reverse('ngo-donation'))

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('ngo-dashboard')
        else:
            print('form invalid')
    return render(request,'ngo_notice.html',{'form':form})

#for Donar LOGIN SECTION
@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_dashboard_view(request):
    donardata=models.DonarExtra.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'address':donardata[0].address,
        'mobile':donardata[0].mobile,
        'company_name':donardata[0].company_name,
        'notice':notice
    }
    return render(request,'donar_dashboard.html',context=mydict)

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_donation_view(request):
    if request.method == "POST":
        don = models.Donation()
        don.username = request.POST.get('username')
        don.companyName = request.POST.get('companyName')
        don.number = request.POST.get('number')
        don.address = request.POST.get('address')
        don.foodName = request.POST.get('foodName')
        don.inputState = request.POST.get('inputState')
        don.quantity = request.POST.get('quantity')
        don.hours = request.POST.get('hours')
        don.description = request.POST.get('description')

        if len(request.FILES) != 0:
            don.foodImage = request.FILES['foodImage']

        don.save()
        messages.success(request, "Donation Listed Successfully!!")
    return render(request,'donar_donation.html')

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def claimed_donation_view(request):
    # claims=models.NGOExtra.objects.all().filter(claimed=True)
    claims=models.Claim.objects.all()
    return render(request,'claimed_donation.html',{'claims':claims})

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_donation_history_view(request):
    donations = models.Donation.objects.all()

    context = {'donations':donations}
    return render(request,'donar_donation_history.html', context)

# @login_required(login_url='donarlogin')
# @user_passes_test(is_ngo)
# def donar_notice_view(request):
#     return render(request,'ngo_notice.html')

#for about us and contact us
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})
