from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .form import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_http_methods, require_GET
from .models import Profile as userProfile


# user login view
@require_http_methods(["GET", "POST"])
def login_view(request):
    # if user is not yet authenticated show him  or her the login page
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    login(request, user)
                    messages.success(
                        request, message="user %s is successfully connected"
                        % username)
                    return redirect("home")
                except PermissionDenied as error:
                    return f"error is : {error}"
            else:
                messages.warning(
                    request, message="sorry, user %s is not yet registered"
                    % username)
                return redirect("login")
        else:
            context = {}
            return render(request, "user/login.html", context)
    # if user is already authenticated redirect him or her to the home page
    return redirect("home")


# user registration view
@require_http_methods(["GET", "POST"])
def register(request):
    # if user is not yet authenticated show him  or her the register page
    if not request.user.is_authenticated:
        form = UserForm()
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                user = authenticate(
                    request, username=username, password=password)
                try:
                    if user is not None:
                        messages.success(
                            request, message="user %s is registered with success"
                            % username)
                        return redirect("login")
                except ValidationError as error:
                    return HttpResponse({"error ": error})
        context = {"form": form}
        return render(request, "user/register.html", context)
    else:
        # if user is already authenticated redirect him or her to the home page
        return redirect("home")


# user profile view
@login_required(login_url="login")
@require_GET
def profile(request):
    userdata = userProfile.objects.filter(  # pylint: disable=no-member
        author__id=int(request.user.id)).first()
    if userdata:
        context = {"userdata": userdata}
        return render(request, "user/profile.html", context)
    return render(request, "user/profile.html", {"userdata": ""})


# user passwrod change view
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user = request.user.username
        # if there's a complete equivalence between the password and confirm_password fields do further processing
        if password == confirm_password:
            try:
                user = User.objects.filter(id=int(request.user.id)).first()
                user.set_password(str(password))
                user.save()
                messages.success(
                    request, message="user %s your password is successfully changed" % user)
                return redirect("login")
            except PermissionError as error:
                return HttpResponse({"error": error})
    else:
        context = {}
        return render(request, "user/change_password.html", context)


# user create profile view
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def create_profile(request):
    form = ProfileForm()
    if request.method == "POST":
        useform = ProfileForm(request.POST)
        user = request.user
        if useform.is_valid():
            try:
                userprofile = useform.save(commit=False)
                userprofile.author = user
                userprofile.save()
                messages.success(
                    request, message="user %s created a profile" % user.username)
                return redirect("home")
            except ValidationError as error:
                return HttpResponse({"error": error})
    context = {"form": form}
    return render(request, "user/createprofile.html", context)


# user password changing view
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def update_profile(request):
    user_id = request.user.id
    if request.method == "POST":
        phonenumber = request.POST.get("phonenumber")
        proffession = request.POST.get("proffession")
        address = request.POST.get("address")
        userprofile = userProfile.objects.filter(  # pylint: disable=no-member
            author__id=int(user_id)).first()
        try:
            username = userprofile.author.username
            userprofile.phonenumber = phonenumber
            userprofile.proffession = proffession
            userprofile.address = address
            userprofile.save()
            messages.success(
                request, message="user %s is updated with success" % username)
            return redirect("profile")
        except ValidationError as error:
            return HttpResponse({"error": error})
    else:
        userdata = userProfile.objects.filter(  # pylint: disable=no-member
            author__id=user_id).first()
        context = {"userdata": userdata}
        return render(request, "user/updateprofile.html", context)


# search user view
@require_http_methods(["POST"])
def search_user(request):
    username = request.POST.get("username")
    if username is not None:
        return redirect("users_searching", username)
    return HttpResponse({"error": "no match for this username"})


# all users by username view
@require_GET
def users_by_username(request, username):
    users = userProfile.objects.filter(  # pylint: disable=no-member
        author__username__icontains=username).all()
    if len(users) > 0:
        try:
            context = {"users": users}
            return render(request, "user/users_searching.html", context)
        except Exception as error:
            return HttpResponse({"error": error})
    return HttpResponse({"error ": "sorry no user exists by that username"})


# all users views
@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def all_users(request):
    if request.method == "POST":
        ban_user_from_group = request.POST.get("user_group_id")
        ban_user_from_platform = request.POST.get("user_platform_id")
        # delete a user from managers's group make that user also lost all
        # persmissions from that group
        if ban_user_from_group:
            user = User.objects.filter(pk=int(ban_user_from_group)).first()
            is_user_in_group = user.groups.filter(
                name="managers").exists()
            # only a users in the managers group or a user with superuser role or the user itself
            # can remove from the managers group
            if request.user.id == user.id or bool(is_user_in_group) or bool(request.user.is_superuser):
                try:
                    managers_group = Group.objects.filter(
                        name="managers").first()
                    managers_group.user_set.remove(user)
                    messages.success(request, message="user %s is banned from %s' group" % (
                        user.username, managers_group.name))
                    return redirect("allusers")
                except PermissionDenied as error:
                    return HttpResponse({"error": error})
            return HttpResponse({"message": "sorry you are not allowed for deleting users"})
        # delete a user from the platform that means that user is banned for real
        # and it needs to register back for regain access
        if ban_user_from_platform:
            user = User.objects.filter(pk=int(request.user.id)).first()
            # only user with superuser role or a user in the managers group that can ban a user
            # from the platform
            if bool(user.is_superuser) or bool(user.has_perm("auth.delete_user")):
                user_to_ban = User.objects.filter(
                    pk=int(ban_user_from_platform)).first()
                managers_group = Group.objects.filter(name="managers").first()
                username = user_to_ban.username
                is_user_in_managers = user_to_ban.groups.filter(
                    name="managers").exists()
                try:
                    # remove the user from the manager's group first if it exists
                    if bool(is_user_in_managers):
                        managers_group.user_set.remove(user_to_ban)
                    # then delete the user from the platform
                    user_to_ban.delete()
                    messages.success(
                        request, message="user %s is banned from the Thirdy platform" % username)
                    return redirect("allusers")
                except PermissionDenied as error:
                    return HttpResponse({"error ": error})
            return HttpResponse({"message": "sorry you're not allowed"})
    else:
        users = userProfile.objects.all()  # pylint: disable=no-member
        context = {"users": users}
        return render(request, "user/allusers.html", context)


# user logout view
def logOut(request):
    logout(request)
    return redirect("login")
