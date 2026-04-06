from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django import forms as dj_forms


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].widget = dj_forms.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Usuário", "autofocus": True}
        )
        form.fields["password"].widget = dj_forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Senha"}
        )
        return form
