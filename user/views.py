import secrets

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from config.settings import EMAIL_HOST_USER
from user.forms import UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from user.models import User


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/check_email/{token}"
        send_mail(
            subject='Подвтердите регистрацию на сайте',
            message=f"Чтобы подтвердить регистрацию, пройдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('user:login'))
