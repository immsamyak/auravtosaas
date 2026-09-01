from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from apps.accounts.models import ConsumerProfile
from apps.brands.models import Brand
from apps.core.models import Testimonial
from apps.core.notifications import NotificationManager
from apps.recommendations.engine import analyze_body_proportions
import random

def signup_view(request):
    if request.method == 'POST':
        # Simple prototyping signup
        username = request.POST.get('username')
        password = request.POST.get('password')
        brand_name = request.POST.get('brand_name')
        email = request.POST.get('email')
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            slug = slugify(brand_name)
            brand = Brand.objects.create(owner=user, name=brand_name, slug=slug, contact_email=email)
            
            # Send Welcome Notification
            NotificationManager.send_welcome_email(user, brand)
            
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/signup.html', {'testimonial': Testimonial.objects.filter(is_active=True).order_by('?').first()})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            # Reset failed login count
            request.session['failed_logins'] = 0
            
            login(request, user)
            
            # Honor 'next' parameter if present
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                from django.utils.http import url_has_allowed_host_and_scheme
                if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                    
            # Admin role redirect
            if user.is_superuser or user.groups.filter(name='Platform Admin').exists():
                return redirect('admin:dashboard')
                
            return redirect('dashboard')
        else:
            # Handle failed login
            failed_logins = request.session.get('failed_logins', 0) + 1
            request.session['failed_logins'] = failed_logins
            
            if failed_logins >= 5:
                # Try to find user to send email
                try:
                    u_obj = User.objects.get(username=u)
                    from apps.core.email_utils import dispatch_async_email
                    context = {
                        'user': u_obj,
                        'reason': 'Multiple failed login attempts'
                    }
                    dispatch_async_email('account_locked', context, [u_obj.email])
                    messages.error(request, "Too many failed attempts. For your security, an alert has been sent to your email.")
                except User.DoesNotExist:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html', {'trusted_brands': Brand.objects.exclude(logo='').order_by('-created_at')[:4]})

def logout_view(request):
    logout(request)
    return redirect('index')

from apps.fitting.models import FitPassport, VTOPhotoVault, VirtualTryOn

@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    profile, created = ConsumerProfile.objects.get_or_create(user=user)
    passport, created_passport = FitPassport.objects.get_or_create(user=user)
    
    if request.method == 'POST' and request.FILES.get('base_photo'):
        uploaded_file = request.FILES['base_photo']
        
        # Create a new VTOPhotoVault entry
        vault_entry = VTOPhotoVault.objects.create(
            passport=passport,
            image=uploaded_file,
            is_default=True
        )
        
        # Trigger Python Computer Vision script
        measurements = analyze_body_proportions(vault_entry.image.path)
        passport.shoulder_width_cm = measurements.get('shoulder_width_cm')
        passport.waist_cm = measurements.get('waist_cm')
        passport.save()
        
        profile.skin_tone_category = measurements.get('skin_tone_category')
        profile.save()
        
        return redirect('profile')
        
    # Get all Try-Ons linked to the user's sessions
    try_ons = VirtualTryOn.objects.filter(session__passport=passport).order_by('-created_at')
    
    # Get the default photo vault
    default_photo = passport.photos.filter(is_default=True).first()
        
    context = {
        'profile': profile,
        'passport': passport,
        'default_photo': default_photo,
        'try_ons': try_ons,
    }
    return render(request, 'accounts/profile.html', context)

from django.contrib.auth.models import User
from django.contrib import messages
from apps.core.email_utils import send_dynamic_email
from .models import PasswordResetOTP
import logging

logger = logging.getLogger(__name__)

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.generate_otp(user)
            
            # Send Email
            try:
                from apps.core.email_utils import dispatch_async_email
                context = {
                    'user': user,
                    'reset_url': otp.otp_code  # Pass OTP code as the URL (MVP approach)
                }
                # No brand specified since it's an account level email
                dispatch_async_email('password_reset', context, [user.email])
            except Exception as e:
                logger.error(f"Failed to send OTP email: {e}")
                # We won't block the user in dev if SMTP fails, but log it.
                print(f"DEV MODE OTP for {user.username}: {otp.otp_code}")

            request.session['reset_email'] = user.email
            return redirect('verify_otp')
        except User.DoesNotExist:
            # Prevent email enumeration by still saying we sent it
            messages.success(request, "If an account exists with that email, an OTP has been sent.")
            return redirect('verify_otp')
            
    return render(request, 'accounts/forgot_password.html')


def verify_otp_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.objects.filter(user=user, otp_code=otp_code, is_used=False).last()
            
            if otp and otp.is_valid():
                otp.is_used = True
                otp.save()
                request.session['can_reset_password'] = True
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired verification code.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
    return render(request, 'accounts/verify_otp.html', {'email': email})


def reset_password_view(request):
    if not request.session.get('can_reset_password'):
        return redirect('forgot_password')
        
    email = request.session.get('reset_email')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password and len(password) >= 8:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                
                # Clean up session
                del request.session['reset_email']
                del request.session['can_reset_password']
                
                messages.success(request, "Your password has been reset successfully. Please log in.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Error finding user.")
        else:
            messages.error(request, "Passwords do not match or are too short.")
            
    return render(request, 'accounts/reset_password.html')
