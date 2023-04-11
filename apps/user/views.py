from datetime import timedelta
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site

from django.http import BadHeaderError, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string

from django.utils import timezone
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import FormView, CreateView, UpdateView

from .models import LoginAttempt, User, UserActivity

from .decorators import unauthenticated_user
from .forms import LoginForm, RegistrationForm, UserEditForm, UserForm
from .token import account_activation_token
from .utils import send_user_email


@unauthenticated_user
def my_login_page(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            now = timezone.now()
            try:
                _user = User.objects.get(email=email)
                login_attempt, created = LoginAttempt.objects.get_or_create(
                    user=_user
                )  # get the user's login attempt
                if (
                    login_attempt.timestamp
                    + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)
                ) < now:
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        login_attempt.login_attempts = 0  # reset the login attempts
                        login_attempt.save()
                        return redirect(
                            "hotel:homepage"
                        )  # change expected_url in your project
                    else:
                        # if the password is incorrect, increment the login attempts and
                        # if the login attempts == MAX_LOGIN_ATTEMPTS, set the user to be inactive and send activation email
                        login_attempt.login_attempts += 1
                        login_attempt.timestamp = now
                        login_attempt.save()
                        if login_attempt.login_attempts == settings.MAX_LOGIN_ATTEMPTS:
                            _user.is_active = False
                            _user.save()
                            # send the re-activation email
                            mail_subject = "Account suspended"
                            current_site = get_current_site(request)
                            send_user_email(
                                _user,
                                mail_subject,
                                email,
                                current_site,
                                "users/email_account_suspended.html",
                            )
                            messages.error(
                                request,
                                "Account suspended, maximum login attempts exceeded. "
                                "Reactivation link has been sent to your email",
                            )
                        else:
                            messages.error(request, "Incorrect email or password")
                            return redirect(settings.LOGIN_URL)
                else:
                    messages.error(request, "Login failed, please try again")
                    return redirect(settings.LOGIN_URL)

            except ObjectDoesNotExist:
                messages.error(request, "Try Incorrect email or password")
                return redirect(settings.LOGIN_URL)
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
    context = {"form": form}
    return render(request, "users/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


# @login_required(login_url="user:login")
# def update_profile(request):
#     if request.method == "POST":
#         u_form = UserEditForm(request.POST, instance=request.user)
#         p_form = ProfileForm(request.POST, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, "Your Account has been updated successfully")
#             return redirect("dashboard:main-dashboard")
#     else:
#         u_form = UserEditForm(instance=request.user)
#         p_form = ProfileForm(instance=request.user.profile)
#     context = {
#         "u_form": u_form,
#         "p_form": p_form,
#     }
#     return render(request, "user/profiles.html", context)


@login_required
def user_update(request, pk):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "User Profile Information Has been Updated Successfully"
            )
            return redirect("profiles:user-profiles")
    else:
        form = UserEditForm(instance=request.user)
    context = {
        "u_form": form,
    }

    context = {"form": form}
    return render(request, "user/update-profiles.html", context)


@login_required
def delete_user(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        delete_message = "Account will be rendered inactive for 3days before deleting. if you wish to recover account, Please contact the admin or use the reactivate account_link"
        messages.success(request, delete_message)
        return redirect("accounts:login")

    return render(request, "users/delete.html")


def activate_account_page(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login_attempt, created = LoginAttempt.objects.get_or_create(user=user)
        if login_attempt.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            login_attempt.login_attempts = 0
            login_attempt.save()
            messages.success(request, "Account restored, you can now proceed to login")
        else:
            messages.success(
                request,
                "Thank you for confirming your email. You can now proceed to Required Registration.",
            )
        return redirect("accounts:login")
    else:
        messages.error(
            request,
            "Thank you for confirming your email. You can now proceed to Required Registration.",
        )
        return redirect("accounts:login")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            logout(request)
        else:
            messages.error(request, "Invalid Details. Please Try Again")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


def handler404(request, exception):
    return render(request, "404.html")


def handle_server_error(request):
    return render(request, "500.html")


@unauthenticated_user
def signup_page(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            to_email = form.cleaned_data.get("email")
            current_site = get_current_site(request)
            mail_subject = "Account Activation"
            response = send_user_email(
                user,
                mail_subject,
                to_email,
                current_site,
                "users/email_verification.html",
            )
            if response == "success":
                messages.success(
                    request,
                    "We have sent you an activation link in your email. Please confirm your"
                    "email before continuing Your Registration Process. Check your spam folder if you don't receive it",
                )
                return redirect("accounts:login")
            else:
                messages.error(
                    request,
                    "An error occurred. Please ensure you have good internet connection and you have entered a valid email address",
                )
                user.delete()
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
            form = RegistrationForm()

    context = {"form": form}
    return render(request, "users/signup.html", context)
