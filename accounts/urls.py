from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  
from .views import custom_logout, profile_view, book_appointment, view_bookings, manage_skills, search_mentors, confirm_booking, reject_booking


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('search-mentors/', search_mentors, name='search_mentors'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('bookings/', view_bookings, name='view_bookings'),
    path('confirm-booking/<int:booking_id>/', confirm_booking, name='confirm_booking'),
    path('reject-booking/<int:booking_id>/', reject_booking, name='reject_booking'),
    path('manage-skills/', manage_skills, name='manage_skills'),
]
