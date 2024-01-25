from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.http import require_POST
from .models import UserProfile,Radio
from .forms import SignUpForm,LoginForm
from django.contrib.auth.models import User


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, department=form.cleaned_data['department'])
            auth_login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('index:login')
            # Redirect based on department
            # if user.profile.department == 'masteruser':
            #     users = User.objects.all()
            #     return render(request, 'login/master.html', {'users': users})
            # elif user.profile.department == 'accounts':
            #     return redirect('index:accounts')
            # elif user.profile.department == 'logistics':
            #     return redirect('index:logistics')
            # elif user.profile.department == 'procurement':
            #     return redirect('index:procurement')
            # elif user.profile.department == 'management':
            #     return redirect('index:management')

    else:
        print('kumar')
        form = SignUpForm()
    return render(request, 'login/signup.html', {'form': form})
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.department == 'masteruser':
                        users = User.objects.select_related('profile').all()
                        radio  = Radio.objects.get(id=1)
                        print('start')
                        print(radio)
                        print('end')
                        return render(request, 'login/master.html', {'users': users,'radio':radio})
                    elif user_profile.department == 'accounts':
                        users = User.objects.select_related('profile').all()
                        radio  = Radio.objects.get(id=1)
                        print('start')
                        print(radio)
                        print('end')
                        return redirect('Accounts:index')
                    elif user_profile.department == 'logistics':
                        users = User.objects.select_related('profile').all()
                        radio  = Radio.objects.get(id=1)
                        print('start')
                        print(radio)
                        print('end')
                        return redirect('Logistics:logindex')
                    # Handle other departments as needed
                except UserProfile.DoesNotExist:
                    messages.error(request, 'User profile not found.')
            else:
                messages.error(request, 'User details not found.')
    else:
        form = LoginForm()

    # Add this block to handle unauthorized access attempts
    # if request.user.is_authenticated:
    #     return redirect('index:login')
    radio  = Radio.objects.get(id=1)
    print('start')
    print(radio)
    print('end')
    return render(request, 'login/login.html', {'form': form,'radio':radio})

# @login_required(login_url='index:login')  # Specify the login URL for redirection
# def index(request):
#     return render(request, 'login/index.html')
@csrf_protect
def user_logout(request):
    logout(request)
    return redirect('index:login')

@login_required(login_url='index:login')
def master(request):
    return render(request, 'login/master.html')



@login_required(login_url='index:login')
def user_delete_view(request, user_id):
    # Ensure that only 'masteruser' can access this view
    if not request.user.profile.department == 'masteruser':
        return redirect('index:login')

    user = get_object_or_404(User, id=user_id)

    # Check if the user has a profile and delete it
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
    except UserProfile.DoesNotExist:
        pass

    # Delete the user
    user.delete()
    users = User.objects.select_related('profile').all()
    messages.success(request, 'User deleted successfully.')
    return render(request, 'login/master.html', {'users': users})

@csrf_exempt
@require_POST
@login_required(login_url='index:login')
def updatelogin(request):
    if request.method == 'POST':
        option_value = request.POST.get('signup-option')

        # Assuming you have a Radio model instance associated with the user
        radio_instance, created = Radio.objects.get_or_create(id=1)

        # Update the radio option
        radio_instance.radio = option_value
        radio_instance.save()

        users = User.objects.select_related('profile').all()
        radio = Radio.objects.get(id=1)

        # Redirect after a successful POST (PRG pattern)
        return redirect('index:master')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})