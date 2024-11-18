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
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'advocateregister.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

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

    return render(request, 'advocateregister.html',)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Attempt to authenticate the user
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
                        if user_profile:
                            return redirect('userDashboard')
                        
                    except UserProfile.DoesNotExist:
                        messages.error(request, 'No associated profile found.')
                        return redirect('login')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, "login.html")

def advocate_adshboard(request):
    return render(request,'advocate/dashboard.html')

def adminDashboard(request):
    if not request.user.is_superuser:
        return redirect('adminDashboard')  # Redirect non-superusers to home

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_pic = request.FILES.get('profile_pic')

        # Basic validation
        if not username or not password or not email:
            messages.error(request, "Username, email, and password are required.")
            return render(request, 'user/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'user/register.html')

        try:
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
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
    
    # Get search parameters from the request
    city = request.GET.get('city')
    # experience = request.GET.get('experience')
    practice_area = request.GET.get('practice_area')

    # Filter advocates based on location
    if city:
        # location_parts = city.split(',')
        
        advocates = Advocate.objects.filter(city__icontains=city)
            # models.Q(location__state__icontains=location_parts[0].strip()) |
            # models.Q(location__country__icontains=location_parts[0].strip())
    

    # Filter by years of experience
    # if experience:
    #     try:
    #         experience = int(experience)
    #         advocates = advocates.filter(experience__gte=experience)
    #     except ValueError:
    #         pass

    # Filter by practice area
    if practice_area:
        advocates = advocates.filter(practice_area__icontains=practice_area.strip())

    return render(request, 'user/view_advocates.html', {'advocates': advocates})


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
def delete_user_profile(request):
    if request.method == 'POST':
        # Get the user profile and user
        user_profile = request.user.userprofile
        user = request.user

        # Delete the user profile and the user account
        user_profile.delete()
        user.delete()

        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Change 'home' to your desired redirect URL

    return render(request, 'user/delete_profile_confirm.html')

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
        # Update the fields from the request
        user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
        user_profile.last_name = request.POST.get('last_name', user_profile.last_name)
        
        # Update email for the user (User model)
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            
        phone_number = request.POST.get('phone_number')
        if phone_number:
            user_profile.phone_number = phone_number
        # Handle profile picture upload
        if request.FILES.get('profile_pic'):
            user_profile.profile_pic = request.FILES['profile_pic']

        user_profile.save()  # Save the updated profile
        return redirect('view_user_profile')  # Redirect to a profile page or success page
    
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

import datetime
@login_required
def chat_room_list(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    advocate = Advocate.objects.filter(advocate=user).first()

    # Get chat rooms where the user is either a UserProfile or Advocate
    if user_profile:
        chat_rooms = ChatRoom.objects.filter(user_profile=user_profile)
    elif advocate:
        chat_rooms = ChatRoom.objects.filter(advocate=advocate)
    else:
        chat_rooms = []

    return render(request, 'chat/chat_room_list.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room_detail(request, advocate_id):
    # Get the UserProfile for the logged-in user
    user_profile = UserProfile.objects.filter(user=request.user).first()
    # Get the Advocate object using advocate_id
    advocate = get_object_or_404(Advocate, id=advocate_id)

    # Check if a chat room exists between the user profile and the advocate
    chat_room, created = ChatRoom.objects.get_or_create(user_profile=user_profile, advocate=advocate)

    # Retrieve all messages in the chat room
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')

    return render(request, 'chat/chat_room_detail.html', {
        'chat_room': chat_room,
        'messages': messages
    })
    
from django.utils import timezone

@login_required
def send_message(request, room_id):
    # Get the chat room by ID or return 404 if not found
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    # Check if the logged-in user is part of the chat room
    if chat_room.user_profile.user != request.user and chat_room.advocate.advocate != request.user:
        return redirect('chat_room_list')  # Redirect if user is unauthorized

    # Process the POST request to send a message
    if request.method == "POST":
        content = request.POST.get('content', '').strip()

        if content:
            # Determine sender and recipient
            sender = request.user
            recipient = chat_room.advocate.advocate if sender == chat_room.user_profile.user else chat_room.user_profile.user

            # Create and save the message
            Message.objects.create(
                chat_room=chat_room,
                sender=sender,
                recipient=recipient,
                content=content,
                created_at=timezone.now()
            )
            # Redirect back to the chat room detail view to display the message
            return redirect('chat_room_detail', advocate_id=chat_room.advocate.id)

    # If GET request or content is empty, just redirect to the chat room
    return redirect('chat_room_detail', advocate_id=chat_room.advocate.id)


@login_required
def advocate_message_list(request):
    # Get the Advocate instance for the logged-in user
    advocate = Advocate.objects.filter(advocate=request.user).first()
    if not advocate:
        return redirect('home')  # Redirect if the user is not an advocate

    # Get all chat rooms associated with this advocate
    chat_rooms = ChatRoom.objects.filter(advocate=advocate)

    return render(request, 'advocate/message_list.html', {
        'chat_rooms': chat_rooms
    })

@login_required
def advocate_chat_room_detail(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    # Ensure the advocate is part of the chat room
    if chat_room.advocate.advocate != request.user:
        return redirect('advocate_message_list')

    # Retrieve all messages in the chat room
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')

    if request.method == "POST":
        content = request.POST.get('content', '').strip()
        if content:
            # Set the sender and recipient
            sender = request.user
            recipient = chat_room.user_profile.user

            # Create a new message
            Message.objects.create(
                chat_room=chat_room,
                sender=sender,
                recipient=recipient,
                content=content,
                created_at=timezone.now()
            )
            return redirect('advocate_chat_room_detail', room_id=room_id)

    return render(request, 'advocate/chat_room_detail.html', {
        'chat_room': chat_room,
        'messages': messages
    })