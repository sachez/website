from django import forms
from payments import models as m
from payments.models import Credit, VerificationInformation, ExtUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ExtUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password123123"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"/admin/password_change/\">Change password</a>"))

    class Meta:
        model = ExtUser
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class Register(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'user@mail.ru',
            'class': 'form-control'
        })
    )
    pas = forms.CharField(widget=forms.PasswordInput({
            'placeholder': 'password',
            'class': 'form-control'
        })
    )
    ver_pas = forms.CharField(widget=forms.PasswordInput({
            'placeholder': 'Retry password',
            'class': 'form-control'
        })
    )
    conv = forms.BooleanField(widget=forms.CheckboxInput({
        'class': 'form-check-input'
    }))


class SignInForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'user@mail.ru',
            'class': 'form-control',
        })
    )
    pas = forms.CharField(widget=forms.PasswordInput({
            'placeholder': 'password',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        pas = cleaned_data.get('pas')
        if ExtUser.objects.filter(email=email).exists():
            if not ExtUser.objects.get(email=email).check_password(pas):
                raise forms.ValidationError('Password or Email is wrong')
        else:
            raise forms.ValidationError('Password or Email is wrong')
        return cleaned_data


class TakeCreditForm(forms.ModelForm):

    deposit = forms.CharField(widget=forms.Select(
        choices=m.Credit.CURRENCYS,
        attrs={
            'class': 'form-control'
        }))

    summary_depos = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))

    lain = forms.CharField(widget=forms.Select(
        choices=m.Credit.LAIN_CURRENCY,
        attrs={
            'class': 'form-control'
        }))

    max_lain = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))

    format_lain = forms.CharField(widget=forms.Select(
        choices=m.Credit.LAIN_FORMAT,
        attrs={
            'class': 'form-control',
        }))

    time_lain = forms.IntegerField(widget=forms.NumberInput({
        'class': 'form-control'
    }))

    class Meta:
        model = Credit
        fields = ('deposit', 'summary_depos', 'lain',
                  'max_lain', 'format_lain', 'time_lain')


class VerificationForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'user@mail.ru',
            'class': 'form-control'
        })
    )

    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'class': 'form-control'
        }))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'FirstName'
        }))

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'LastName'
        }))

    adress = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'adress'
        }))

    pasport = forms.CharField(
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }))

    note_bank = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }))

    class Meta:
        model = VerificationInformation
        fields = ('email', 'first_name', 'last_name',
                  'birth_date', 'adress', 'pasport', 'note_bank')

