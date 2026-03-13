from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import LoginUserForm, NewUserForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def login_user(request):
    if request.user.is_authenticated and not request.user.is_superuser and not 'next' in request.GET: 
        return render(request, 'accounts/login.html', {'error':'You are not allowed'})
    
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Successfully logged in')
                next_url = request.GET.get('next', None)
                if next_url is None:
                    return redirect('/posts')
                else:
                    if user.is_superuser:
                        return redirect(next_url)
                    else:
                        return redirect('/')
            else:
                return render(request, 'accounts/login.html', {'form':form})
        else:
            return render(request, 'accounts/login.html', {'form':form})
    else:    
        form = LoginUserForm()
        return render(request, 'accounts/login.html', {'form':form})


def register_user(request):
    '''if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']
        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/register.html', {'error':'This Username Is Already Exist'})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'accounts/register.html', {'error':'This Email Is Already Exist'})
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    return redirect('/accounts/login')
        else:
            return render(request, 'accounts/register.html', {'error':'Please Enter Your Password Carefully'})
    else:
        return render(request, 'accounts/register.html')'''
        
        
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/register.html', {'form':form})
    else:
        form = NewUserForm()
        return render(request, 'accounts/register.html', {'form':form})
        
        

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
    return redirect('/accounts/login')
           
                
            

