from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Extract advocate-specific data
        id_card = request.POST['id_card']
        practice_area = request.POST['practice_area']
        experience = request.POST['experience']
        achievements = request.POST['achievements']
        languages = request.POST['languages']
        courts = request.POST['courts']
        address = request.POST['address']
        city = request.POST['city']
        pin = request.POST['pin']
        mobile = request.POST['mobile']
        location_id = request.POST['location']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'advocateregister.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        location = Location.objects.get(id=location_id)
        advocate = Advocate(
            advocate=user,
            id_card=id_card,
            practice_area=practice_area,
            experience=experience,
            achievements=achievements,
            languages=languages,
            courts=courts,
            address=address,
            city=city,
            pin=pin,
            mobile=mobile,
            location=location
        )
        advocate.save()

        # Authenticate and log in the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Registration Successfull")
            return redirect('login')
        else:
            messages.error(request, "Login failed. Please try again.")
            return redirect('login')  # Redirect to login page if authentication fails

    locations = Location.objects.all()
    return render(request, 'advocateregister.html', {'locations': locations})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)

        if user.is_superuser:
            return redirect('adminDashboard')
        else:
            # Check if the user is an advocate
            try:
                advocate = Advocate.objects.get(advocate=user)
                if advocate.approved:  # Check if the advocate is approved
                    return redirect('advocateDashboard')
                else:
                    messages.error(request, 'Your advocate account is not approved.')
                    return redirect('login')
            except Advocate.DoesNotExist:
                # Check if the user is a regular user
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile:  # Check if the user profile is approved
                        return redirect('userDashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, 'Invalid username or password.')
                    return redirect('login')

    return render(request, "login.html")

def advocate_adshboard(request):
    return render(request,'advocate/dashboard.html')

def adminDashboard(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-superusers to home

    # Fetch all advocates and users
    advocates = Advocate.objects.all()  # Fetch all advocates
    users = User.objects.all()  # Fetch all users (Django's default User model)

    return render(request, 'admin/dashboard.html', {'advocates': advocates, 'users': users})

def approve_advocate(request,advocate_id):
    advocate = Advocate.objects.get(id=advocate_id)
    advocate.approved=True
    advocate.save()
    return redirect('adminDashboard')

def add_case(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        advocate = Advocate.objects.get(user=request.user)

        new_case = Case(title=title, description=description, advocate=advocate)
        new_case.save()
        messages.success(request, 'Case added successfully!')
        return redirect('dashboard')

    return render(request, 'advocate/add_case.html')

@login_required
def view_cases(request):
    advocate = Advocate.objects.get(user=request.user)
    cases = advocate.cases.all()
    return render(request, 'advocate/view_cases.html', {'cases': cases})

@login_required
def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        case.title = request.POST.get('title')
        case.description = request.POST.get('description')
        case.status = request.POST.get('status')
        case.save()
        messages.success(request, 'Case updated successfully!')
        return redirect('view_cases')

    return render(request, 'advocate/edit_case.html', {'case': case})

@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    messages.success(request, 'Case deleted successfully!')
    return redirect('view_cases')

def logout_view(request):
    logout(request)
    return redirect('home')

def  home(request):
    return render(request,'index.html')

def  services(request):
    return render(request,'services.html')

def  about(request):
    return render(request,'about.html')

def case_studies(request):
    # Fetch the 3 most recent cases
    recent_cases = Case.objects.order_by('-created_at')[:3]  # Adjust the number as needed
    context = {
        'recent_cases': recent_cases,
    }
    return render(request, 'caseStudies.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation (you can enhance this)
        if name and email and phone and subject and message:
            contact = Contact(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            contact.save()  # Save the contact data to the database
            return redirect('home')  # Redirect to a success page

        else:
            error_message = "All fields are required."
            return render(request, 'contact.html', {'error': error_message})  # Return form with error

    return render(request, 'contact.html')


#_---------------------------------------------------------------------------------------------------------------
def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_pic = request.FILES.get('profile_pic')

        try:
            # Create user
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create UserProfile
            UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name, profile_pic=profile_pic)

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration

        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'user/register.html')

def case_application(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        advocate_id = request.POST.get('advocate')  # Assuming advocate ID is passed

        # Basic validation
        if title and description and advocate_id:
            case = Case(
                title=title,
                description=description,
                advocate_id=advocate_id,  # Associate with the selected advocate
                status='Open'  # Default status
            )
            case.save()
            return redirect('home')  # Redirect to a desired page after case application

        # Render the form with an error message if validation fails
        error_message = "Please provide all required information."
        return render(request, 'cases/apply.html', {'error': error_message})

    return render(request, 'cases/apply.html')

def userDashboard(request):
    return render (request,"user/dashboard.html")

def advocateDashboard(request):
    return render(request,"advocate/dashboard.html")

def approve_user(request, first_name):
    # Get the user profile or return a 404 if not found
    user_profile = get_object_or_404(UserProfile, id=first_name)
    user_profile.approved = True
    user_profile.save()
    
    # Optionally, you can add a success message here
    messages.success(request, f"{user_profile.first_name} {user_profile.last_name} has been approved.")
    
    return redirect('adminDashboard')  # Redirect to the admin dashboard

def view_all_cases(request):
    # Retrieve all case instances
    cases = Case.objects.all()

    # Render the cases in a template
    return render(request, 'user/view_cases.html', {'cases': cases})

def view_advocates(request):
    advocates = Advocate.objects.all()
    return render(request, 'user/view_advocates.html', {'advocates': advocates})

@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)

    if request.method == 'POST':
        # Directly getting content from the POST request
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('view_sent_messages')  # Redirect to the messages view
        else:
            messages.error(request, 'Message cannot be empty.')

    return render(request, 'send_messages.html', {'recipient': recipient})

@login_required
def view_sent_messages(request):
    # Fetch messages sent by the logged-in user
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'view_sent_messages.html', {'messages': messages})

@login_required
def view_received_messages(request):
    # Fetch messages received by the logged-in user
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'view_received_messages.html', {'messages': messages})

def view_all_users(request):
    users  = UserProfile.objects.all()
    return render(request,"admin/users.html",{"users":users})

def view_all_advocates(request):
    advocates  = Advocate.objects.all()
    return render(request,"admin/advocates.html",{"advocates":advocates})

# Update user data
def update_user(request, user_id):
    if request.method == "POST":
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        user_profile.first_name = request.POST.get("first_name", user_profile.first_name)
        user_profile.last_name = request.POST.get("last_name", user_profile.last_name)
        user_profile.save()
        return HttpResponse("User updated successfully!")
    return HttpResponse("Invalid request!", status=400)

# Delete user
def delete_user(request, user_id):
    if request.method == "POST":
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        user_profile.delete()
        return HttpResponse("User deleted successfully!")
    return HttpResponse("Invalid request!", status=400)

@login_required
def update_advocate(request, advocate_id):
    advocate = get_object_or_404(Advocate, id=advocate_id)
    if request.method == "POST":
        advocate.id_card = request.POST.get("id_card")
        advocate.practice_area = request.POST.get("practice_area")
        advocate.experience = request.POST.get("experience")
        advocate.achievements = request.POST.get("achievements")
        advocate.languages = request.POST.get("languages")
        advocate.courts = request.POST.get("courts")
        advocate.address = request.POST.get("address")
        advocate.city = request.POST.get("city")
        advocate.pin = request.POST.get("pin")
        advocate.mobile = request.POST.get("mobile")
        advocate.save()
        return redirect(reverse('advocate_list'))  # Redirect to the list view or desired page

    return redirect(reverse('view_all_advocates'))

@login_required
def delete_advocate(request, advocate_id):
    advocate = get_object_or_404(Advocate, id=advocate_id)
    advocate.delete()
    return redirect('view_all_advocates')

# Views for User Profile
@login_required
def view_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/user_profile.html', {'user_profile': user_profile})

@login_required
def update_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        if request.FILES.get('profile_pic'):
            user_profile.profile_pic = request.FILES.get('profile_pic')
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_user_profile')
    return render(request, 'user/user_profile.html', {'user_profile': user_profile})

@login_required
def change_user_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user
        if check_password(current_password, user.password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password changed successfully!')
        else:
            messages.error(request, 'Current password is incorrect.')
    return redirect('view_user_profile')

@login_required
def view_advocate_profile(request):
    advocate_profile = Advocate.objects.get(advocate=request.user)
    return render(request, 'advocate/advocate_profile.html', {'advocate_profile': advocate_profile})

@login_required
def update_advocate_profile(request):
    advocate_profile = Advocate.objects.get(advocate=request.user)
    if request.method == 'POST':
        advocate_profile.id_card = request.POST.get('id_card')
        advocate_profile.practice_area = request.POST.get('practice_area')
        advocate_profile.experience = request.POST.get('experience')
        advocate_profile.achievements = request.POST.get('achievements')
        advocate_profile.languages = request.POST.get('languages')
        advocate_profile.courts = request.POST.get('courts')
        advocate_profile.address = request.POST.get('address')
        advocate_profile.city = request.POST.get('city')
        advocate_profile.pin = request.POST.get('pin')
        advocate_profile.mobile = request.POST.get('mobile')
        advocate_profile.save()
        messages.success(request, 'Advocate profile updated successfully!')
        return redirect('view_advocate_profile')
    return render(request, 'advocate/advocate_profile.html', {'advocate_profile': advocate_profile})

@login_required
def change_advocate_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        advocate = request.user
        if check_password(current_password, advocate.password):
            advocate.set_password(new_password)
            advocate.save()
            update_session_auth_hash(request, advocate)  # Important!
            messages.success(request, 'Password changed successfully!')
        else:
            messages.error(request, 'Current password is incorrect.')
    return redirect('view_advocate_profile')