from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Muvaffaqiyatli login amalga oshirildi!")
                    return redirect("home")
                else:
                    messages.warning(request, "Sizning akkountingiz faol emas.")
            else:
                messages.error(request, "Login yoki parol noto‘g‘ri!")
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. Endi login qiling.")
            return redirect("login")
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect("profile", request.user.id)
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "pages/profile_edit.html", {
        "user_form": user_form,
        "user": request.user
    })
