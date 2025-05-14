from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile, Skill, Booking

# Home view
def home(request):
    return render(request, 'accounts/home.html')

# Register view (creating user and profile)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            # Create an empty profile for the user
            Profile.objects.create(user=user)
            # Log the user in
            from django.contrib.auth import login
            login(request, user)
            # Redirect to profile setup
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Dashboard view (user's profile and additional content)
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if not hasattr(user, 'profile'):
        return redirect('profile')  # Redirect to profile creation if no profile exists
    return render(request, 'accounts/dashboard.html')

# Custom logout view
def custom_logout(request):
    logout(request)
    return redirect('home')

# Profile view (edit profile details)
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    # Try to get the user's profile, if it exists
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # If profile doesn't exist, create one
        profile = Profile.objects.create(user=user)

    # Check if this is the first time setting up the profile
    is_first_setup = not profile.bio and not profile.user_type and not profile.skills.exists()

    # Create some default skills if none exist
    if Skill.objects.count() == 0:
        default_skills = [
            "Python", "Django", "JavaScript", "React", "HTML/CSS",
            "Data Science", "Machine Learning", "UI/UX Design", 
            "Mobile Development", "DevOps"
        ]
        for skill_name in default_skills:
            Skill.objects.create(name=skill_name)

    # Handle form submission to update profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = user  # Set the user for the profile
            prof.save()
            
            # Handle skills separately to ensure they're saved correctly
            selected_skills = request.POST.getlist('skills')
            profile.skills.clear()  # Remove existing skills
            for skill_id in selected_skills:
                try:
                    skill = Skill.objects.get(id=skill_id)
                    profile.skills.add(skill)
                except Skill.DoesNotExist:
                    pass
            
            return redirect('dashboard')  # Redirect to the dashboard after saving the profile
    else:
        form = ProfileForm(instance=profile)

    # Render the profile edit form
    return render(request, 'accounts/profile.html', {
        'form': form,
        'is_first_setup': is_first_setup,
        'all_skills': Skill.objects.all()
    })

# View for searching mentors by skill
@login_required(login_url='login')
def search_mentors(request):
    # Get all available skills for the filter dropdown
    all_skills = Skill.objects.all()
    
    # Initialize an empty queryset
    mentors = []
    selected_skill = None
    
    # Check if a skill filter was applied
    if request.method == 'GET' and 'skill' in request.GET:
        skill_id = request.GET.get('skill')
        if skill_id:
            try:
                # Get the selected skill
                selected_skill = Skill.objects.get(id=skill_id)
                
                # Find all profiles that are mentors and have the selected skill
                mentor_profiles = Profile.objects.filter(
                    user_type='mentor',
                    skills=selected_skill
                )
                
                # Get the users associated with these profiles
                mentors = [profile.user for profile in mentor_profiles]
            except Skill.DoesNotExist:
                # Handle case where skill doesn't exist
                pass
    
    context = {
        'all_skills': all_skills,
        'mentors': mentors,
        'selected_skill': selected_skill
    }
    
    return render(request, 'accounts/search_mentors.html', context)

# View for booking appointments with mentors
@login_required(login_url='login')
def book_appointment(request):
    # Get the mentor ID and skill ID from the URL parameters
    mentor_id = request.GET.get('mentor_id')
    skill_id = request.GET.get('skill_id')
    
    mentor = None
    skill = None
    
    # Validate the mentor and skill
    if mentor_id and skill_id:
        try:
            mentor = User.objects.get(id=mentor_id)
            skill = Skill.objects.get(id=skill_id)
            
            # Verify that the mentor has the specified skill
            if not mentor.profile.skills.filter(id=skill.id).exists():
                mentor = None
                skill = None
        except (User.DoesNotExist, Skill.DoesNotExist):
            mentor = None
            skill = None
    
    # Handle form submission for booking
    if request.method == 'POST' and mentor and skill:
        # Get the scheduled date and time from the form
        scheduled_date = request.POST.get('date')
        scheduled_time = request.POST.get('time')
        
        if scheduled_date and scheduled_time:
            # Combine date and time into a datetime object
            from datetime import datetime
            scheduled_at = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
            
            # Create a new booking
            Booking.objects.create(
                learner=request.user,
                mentor=mentor,
                skill=skill,
                scheduled_at=scheduled_at,
                status='Pending'
            )
            
            # Redirect to the bookings page
            return redirect('view_bookings')
    
    context = {
        'mentor': mentor,
        'skill': skill
    }
    
    return render(request, 'accounts/book_appointment.html', context)

# View for viewing user's bookings
@login_required(login_url='login')
def view_bookings(request):
    # Get the current user
    user = request.user
    
    # Get all bookings where the user is either a learner or a mentor
    learner_bookings = user.bookings.all()
    mentor_appointments = user.appointments.all()
    
    context = {
        'learner_bookings': learner_bookings,
        'mentor_appointments': mentor_appointments
    }
    
    return render(request, 'accounts/view_bookings.html', context)

# View for managing skills
@login_required(login_url='login')
def manage_skills(request):
    # Get the current user's profile
    profile = request.user.profile
    
    # Handle form submission to update skills
    if request.method == 'POST':
        # Process the form data and update the user's skills
        # This is a simplified version; you would need to validate the data
        skill_ids = request.POST.getlist('skills')
        profile.skills.clear()  # Remove all existing skills
        for skill_id in skill_ids:
            profile.skills.add(skill_id)  # Add selected skills
        return redirect('dashboard')
    
    # Get all available skills and the user's current skills
    all_skills = Skill.objects.all()
    user_skills = profile.skills.all()
    
    context = {
        'all_skills': all_skills,
        'user_skills': user_skills
    }
    
    return render(request, 'accounts/manage_skills.html', context)
