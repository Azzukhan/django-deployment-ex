from django.shortcuts import render
from basicapp.form import UserForm, UserProfileInfoForm


from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request,'basicapp/index.html')

def register(request):
    registered = False

    if request.method == 'POST' :

        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile_pic = profile_form.save(commit=False)
            profile_pic.user=user

            if 'profile' in request.FILES:
                profile_pic.profile = request.FILES['profile']
            profile_pic.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basicapp/registertion.html', {'user_form':user_form , 'profile_form':profile_form , 'registered':registered})

@login_required
def special(request):
    return HttpResponse('you are login')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Some tried to login and failed')
            print('UserName:{} and Password:{}'.format(username,password))
            return HttpResponse('Invalid Detail')
    else:
        return render(request,'basicapp/login.html',{})
