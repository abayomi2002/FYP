from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
def home(request):
    
    return redirect('dashboard_view')
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        weight_goal = request.POST.get('weight_goal')
        profile_picture = request.FILES.get('profile_picture')

        print(password)
        
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password= password,
            height=height,
            weight=weight,
            age=age,
            weight_goal=weight_goal,
            profile_picture=profile_picture,
            gender=gender,
        )
        login(request, user)
        return redirect('login')  # Redirect to a dashboard or some other page after signup

    return render(request, 'signup.html')
@login_required(login_url='/login/')
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.height = request.POST.get('height')
        user.weight = request.POST.get('weight')
        user.age = request.POST.get('age')
        user.weight_goal = request.POST.get('weight_goal')
        user.gender = request.POST.get('gender')

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')

        user.save()

        # If the user updates their password
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)
            user.save()
              # Keep the user logged in after changing the password

        return redirect('dashboard_view')  # Redirect to a profile page after updating

    return render(request, 'update_profile.html', {'user': request.user})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        print(username, password, remember_me)

        user = authenticate(request, username=username, password=password)
        print('Request sent successfully')
        if user is not None:
            login(request, user)
            print('authenticated successfully')
            return redirect('dashboard_view')  # Redirect to the desired page after login

        else:
            messages.error(request, 'Invalid email or password')
            return redirect('dashboard')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to the login page after logging out
@login_required(login_url='/login/')
def dashboard_view(request):
    user = CustomUser.objects.get(id=request.user.id)

    # Get today's food logs
    today_logs = FoodLog.objects.filter(user=user)
    print(today_logs)
    # Calculate total calories for today
    total_calories = sum(log.calories for log in today_logs)

    context = {
        'height': user.height,
        'weight': user.weight,
        'age': user.age,
        'weight_goal': user.weight_goal,
        'bmi': user.calculate_bmi(),
        'bmr': user.calculate_bmr(),
        'health_status': user.get_health_status(),
        'overweight_amount': user.overweight_amount(),
        'calories_intake': user.recommended_calorie_intake(),
        'days_to_reach_goal': user.days_to_reach_goal(),
        'today_logs': today_logs,
        'total_calories': total_calories,
    }

    return render(request, 'dashboard.html', context)

def log_food(request):
    if request.method == 'POST':
        food_name = request.POST.get('food_name')
        calories = request.POST.get('calories')
        user = CustomUser.objects.get(id = request.user.id)
        # Create a new FoodLog entry
        FoodLog.objects.create(
            user=user,
            food_name=food_name,
            calories=calories
        )
        return redirect('dashboard_view')  

    return render(request, 'dashboard_view')  # Render the form if the request is GET