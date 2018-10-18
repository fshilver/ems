from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UsernameField


class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'is_active', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('name', 'password', 'is_active', 'is_staff')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.HiddenInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'flat'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'flat'}),
        }


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('name', 'is_active', 'is_staff')
        labels = {
            'name': '이름',
            'is_active': '활성화',
            'is_staff': '팀 관리자',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'flat'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'flat'}),
        }



class SignUpForm(forms.ModelForm):

    field_order = ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'groups')

    groups = forms.ModelMultipleChoiceField(
        label='소속 사업부',
        queryset=None,
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'select2_multiple form-control'}),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        strip=False,
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'is_active', 'is_staff', 'groups')
        labels = {
            'email': 'Email',
            'name': 'Name',
            'is_active': '활성화 여부',
            'is_staff': '팀 관리자 여부',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'flat'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'flat'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['groups'].queryset = Group.objects.all()
            else:
                self.fields['groups'].queryset = Group.objects.filter(user=user)
        else:
            self.fields['groups'].queryset = Group.objects.all()


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['groups'])

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add(*self.cleaned_data['groups']) # groups 는 list 이기 때문에 *self 로 사용
        return user


class LoginForm(AuthenticationForm):

    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
    )

    error_messages = {
        'invalid_login': _(
            "입력하신 Email 과 비밀번호가 맞지 않습니다."
        ),
        'inactive': _("This account is inactive."),
    }
