from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from .models import User, EmailVerification, PasswordReset


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            date_of_birth = request.POST.get('date_of_birth', '')
            learning_goals = request.POST.get('learning_goals', '').strip()

            # Validation
            errors = []

            if not all([first_name, last_name, email, password1, password2]):
                errors.append('All required fields must be filled.')

            if password1 != password2:
                errors.append('Passwords do not match.')

            if len(password1) < 8:
                errors.append('Password must be at least 8 characters long.')

            if User.objects.filter(email=email).exists():
                errors.append('An account with this email already exists.')

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, self.template_name)

            # Auto-generate username from email
            username = User.generate_username_from_email(email)

            # Create user
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    learning_goals=learning_goals
                )

                if date_of_birth:
                    user.date_of_birth = date_of_birth
                    user.save()

                # Create email verification
                verification = EmailVerification.create_verification(user)

                # Send verification email
                self.send_verification_email(user, verification)

                messages.success(request,
                    'Account created successfully! Please check your email to verify your account.')
                return redirect('users:login')

        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, self.template_name)

    def send_verification_email(self, user, verification):
        """Send email verification"""
        try:
            from django.template.loader import render_to_string
            from django.core.mail import EmailMultiAlternatives
            from django.contrib.sites.models import Site

            # Get current site domain
            try:
                current_site = Site.objects.get_current()
                domain = current_site.domain
            except:
                # Fallback to localhost for development
                domain = 'localhost:8000'

            # Build verification URL
            verification_url = f"http://{domain}/auth/verify-email/{verification.token}/"

            # Prepare context for email templates
            context = {
                'user': user,
                'verification_url': verification_url,
                'site_name': 'Mentora',
            }

            # Render email templates
            subject = 'Verify Your Mentora Account'
            text_content = render_to_string('emails/verification_email.txt', context)
            html_content = render_to_string('emails/verification_email.html', context)

            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

        except Exception as e:
            print(f"Failed to send verification email: {e}")


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Please enter both username/email and password.')
            return render(request, self.template_name)

        # Try to authenticate with username or email
        user = authenticate(request, username=username, password=password)

        if not user:
            # Try with email if username failed
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            if user.is_active:
                login(request, user)

                # Set session expiry
                if not remember_me:
                    request.session.set_expiry(0)  # Browser close
                else:
                    request.session.set_expiry(1209600)  # 2 weeks

                # Update last login IP
                user.last_login_ip = self.get_client_ip(request)
                user.save(update_fields=['last_login_ip'])

                messages.success(request, f'Welcome back, {user.first_name}!')

                # Redirect to next or dashboard
                next_url = request.GET.get('next', 'core:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account has been deactivated.')
        else:
            messages.error(request, 'Invalid username/email or password.')

        return render(request, self.template_name)

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.success(request, f'Goodbye, {request.user.first_name}! You have been logged out successfully.')
        logout(request)
        return redirect('core:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add user statistics
        from progress.models import UserProgress, TopicProgress

        total_progress = UserProgress.objects.filter(user=user).count()
        completed_progress = UserProgress.objects.filter(user=user, is_completed=True).count()
        total_topics = TopicProgress.objects.filter(user=user).count()
        completed_topics = TopicProgress.objects.filter(user=user, is_completed=True).count()

        context.update({
            'total_progress': total_progress,
            'completed_progress': completed_progress,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
        })

        return context


class UpdateProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def post(self, request):
        try:
            user = request.user

            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            phone_number = request.POST.get('phone_number', '').strip()
            current_class_level = request.POST.get('current_class_level', '')
            date_of_birth = request.POST.get('date_of_birth', '')

            # Validation
            errors = []

            if not all([first_name, last_name, email]):
                errors.append('First name, last name, and email are required.')

            # Check if email is already taken by another user
            if email != user.email and User.objects.filter(email=email).exists():
                errors.append('This email is already in use by another account.')

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('users:profile')

            # Update user fields
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number if phone_number else None

            if current_class_level:
                user.current_class_level = int(current_class_level)
            else:
                user.current_class_level = None

            if date_of_birth:
                user.date_of_birth = date_of_birth
            else:
                user.date_of_birth = None

            user.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')

        except Exception as e:
            # Log the actual error for debugging
            print(f"Profile update error: {e}")
            messages.error(request, f'An error occurred while updating your profile: {str(e)}')
            return redirect('users:profile')


class VerifyEmailView(View):
    template_name = 'users/verify_email.html'

    def get(self, request, token):
        try:
            verification = get_object_or_404(EmailVerification, token=token, is_used=False)

            if verification.is_expired():
                messages.error(request, 'This verification link has expired. Please request a new one.')
                return redirect('users:resend_verification')

            # Verify the email
            user = verification.user
            user.is_email_verified = True
            user.save()

            verification.is_used = True
            verification.save()

            messages.success(request, 'Your email has been verified successfully!')

            # Auto-login the user
            if not request.user.is_authenticated:
                login(request, user)
                return redirect('core:dashboard')

            return render(request, self.template_name)

        except Exception as e:
            messages.error(request, 'Invalid or expired verification link.')
            return redirect('users:resend_verification')


class ResendVerificationView(View):
    template_name = 'users/resend_verification.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '').strip().lower()

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(email=email)

            if user.is_email_verified:
                messages.info(request, 'Your email is already verified.')
                return redirect('users:login')

            # Create new verification
            verification = EmailVerification.create_verification(user)

            # Send verification email
            self.send_verification_email(user, verification)

            messages.success(request, 'Verification email sent! Please check your inbox.')
            return redirect('users:login')

        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, 'Failed to send verification email. Please try again.')
            return render(request, self.template_name)

    def send_verification_email(self, user, verification):
        """Send email verification"""
        try:
            from django.template.loader import render_to_string
            from django.core.mail import EmailMultiAlternatives
            from django.contrib.sites.models import Site

            # Get current site domain
            try:
                current_site = Site.objects.get_current()
                domain = current_site.domain
            except:
                # Fallback to localhost for development
                domain = 'localhost:8000'

            # Build verification URL
            verification_url = f"http://{domain}/auth/verify-email/{verification.token}/"

            # Prepare context for email templates
            context = {
                'user': user,
                'verification_url': verification_url,
                'site_name': 'Mentora',
            }

            # Render email templates
            subject = 'Verify Your Mentora Account'
            text_content = render_to_string('emails/verification_email.txt', context)
            html_content = render_to_string('emails/verification_email.html', context)

            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

        except Exception as e:
            print(f"Failed to send verification email: {e}")


class PasswordResetView(View):
    template_name = 'users/password_reset.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '').strip().lower()

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, self.template_name)

        try:
            user = User.objects.get(email=email)

            # Create password reset token
            reset = PasswordReset.create_reset(user, self.get_client_ip(request))

            # Send reset email
            self.send_reset_email(user, reset)

            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('users:password_reset_sent')

        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            messages.success(request, 'If an account with this email exists, password reset instructions have been sent.')
            return redirect('users:password_reset_sent')
        except Exception as e:
            messages.error(request, 'Failed to send password reset email. Please try again.')
            return render(request, self.template_name)

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def send_reset_email(self, user, reset):
        """Send password reset email"""
        try:
            subject = 'Reset Your Mentora Password'
            message = f"""
            Hello {user.first_name},

            You requested to reset your password for your Mentora account.

            Click the link below to reset your password:

            http://127.0.0.1:8000/auth/password-reset-confirm/{reset.token}/

            This link will expire in 1 hour for security reasons.

            If you didn't request this password reset, please ignore this email.

            Best regards,
            The Mentora Team
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send password reset email: {e}")


class PasswordResetSentView(TemplateView):
    template_name = 'users/password_reset_sent.html'


class PasswordResetConfirmView(View):
    template_name = 'users/password_reset_confirm.html'

    def get(self, request, token):
        try:
            reset = get_object_or_404(PasswordReset, token=token, is_used=False)

            if reset.is_expired():
                messages.error(request, 'This password reset link has expired. Please request a new one.')
                return redirect('users:password_reset')

            return render(request, self.template_name, {'token': token})

        except Exception as e:
            messages.error(request, 'Invalid or expired password reset link.')
            return redirect('users:password_reset')

    def post(self, request, token):
        try:
            reset = get_object_or_404(PasswordReset, token=token, is_used=False)

            if reset.is_expired():
                messages.error(request, 'This password reset link has expired. Please request a new one.')
                return redirect('users:password_reset')

            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            # Validation
            if not password1 or not password2:
                messages.error(request, 'Please fill in both password fields.')
                return render(request, self.template_name, {'token': token})

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, self.template_name, {'token': token})

            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, self.template_name, {'token': token})

            # Reset password
            user = reset.user
            user.set_password(password1)
            user.save()

            # Mark reset as used
            reset.is_used = True
            reset.save()

            messages.success(request, 'Your password has been reset successfully! You can now sign in with your new password.')
            return redirect('users:password_reset_complete')

        except Exception as e:
            messages.error(request, 'An error occurred while resetting your password. Please try again.')
            return render(request, self.template_name, {'token': token})


class PasswordResetCompleteView(TemplateView):
    template_name = 'users/password_reset_complete.html'


class UserStatsAPIView(LoginRequiredMixin, View):
    """API endpoint for user statistics"""

    def get(self, request):
        try:
            user = request.user

            # Import models here to avoid circular imports
            from progress.models import UserProgress, TopicProgress
            from content.models import Quiz

            # Calculate user statistics
            total_quizzes = Quiz.objects.filter(user=user).count()
            completed_quizzes = Quiz.objects.filter(user=user, is_completed=True).count()
            passed_quizzes = Quiz.objects.filter(user=user, is_completed=True, percentage__gte=70).count()

            # Progress statistics
            total_progress = UserProgress.objects.filter(user=user).count()
            completed_progress = UserProgress.objects.filter(user=user, is_completed=True).count()

            # Topic progress
            total_topics = TopicProgress.objects.filter(user=user).count()
            completed_topics = TopicProgress.objects.filter(user=user, is_completed=True).count()

            # Calculate completion percentage
            completion_percentage = 0
            if total_topics > 0:
                completion_percentage = round((completed_topics / total_topics) * 100, 1)

            # Calculate average score
            avg_score = 0
            if completed_quizzes > 0:
                total_score = sum(quiz.percentage for quiz in Quiz.objects.filter(user=user, is_completed=True))
                avg_score = round(total_score / completed_quizzes, 1)

            # Calculate study time (estimate based on completed activities)
            study_time_hours = completed_quizzes * 0.5 + completed_topics * 0.3  # Rough estimate

            # Format study time
            if study_time_hours < 1:
                study_time = f"{int(study_time_hours * 60)}m"
            else:
                study_time = f"{int(study_time_hours)}h"

            # Calculate achievements (based on milestones)
            achievements = 0
            if completed_quizzes >= 1:
                achievements += 1  # First quiz
            if completed_quizzes >= 5:
                achievements += 1  # Quiz master
            if completed_quizzes >= 10:
                achievements += 1  # Quiz expert
            if avg_score >= 80:
                achievements += 1  # High achiever
            if avg_score >= 90:
                achievements += 1  # Excellence
            if completion_percentage >= 25:
                achievements += 1  # Quarter complete
            if completion_percentage >= 50:
                achievements += 1  # Half complete
            if completion_percentage >= 75:
                achievements += 1  # Almost there
            if completion_percentage >= 100:
                achievements += 1  # Complete mastery

            # Return statistics
            stats = {
                'levels_completed': completed_topics,
                'study_time': study_time,
                'achievements': achievements,
                'total_quizzes': total_quizzes,
                'completed_quizzes': completed_quizzes,
                'passed_quizzes': passed_quizzes,
                'avg_score': avg_score,
                'completion_percentage': completion_percentage,
                'total_topics': total_topics,
                'completed_topics': completed_topics,
            }

            return JsonResponse(stats)

        except Exception as e:
            # Return default values if there's an error
            return JsonResponse({
                'levels_completed': 0,
                'study_time': '0h',
                'achievements': 0,
                'total_quizzes': 0,
                'completed_quizzes': 0,
                'passed_quizzes': 0,
                'avg_score': 0,
                'completion_percentage': 0,
                'total_topics': 0,
                'completed_topics': 0,
                'error': 'Could not load statistics'
            })