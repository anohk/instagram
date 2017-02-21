from django import forms
from django.contrib.auth.password_validation import validate_password

from myuser.models import Myuser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    nickname = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(
        choices=Myuser.CHOICES_GENDER,
        widget=forms.RadioSelect,
    )

    def clean_username(self):
        """
        username field 검증 로직
        :return:
        """
        username = self.cleaned_data['username']
        if Myuser.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists!')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password1)
        if password1 != password2:
            raise forms.ValidationError('password does not match')
        return password1

    def create_user(self):
        username = self.cleaned_data['username']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        nickname = self.cleaned_data['nickname']

        user = Myuser.objects.create_user(
            username=username,
            password=password2,
        )
        user.email = email
        user.gender = gender
        user.nickname = nickname
        user.save()
        return user


class SignupModelForm(forms.ModelForm):
    class Meta:
        model = Myuser
        fields = (
            'username',
            'password',
            'email',
            'gender',
            'nickname',
        )


class ProfileImageForm(forms.Form):
    photo = forms.ImageField()

class ChangeProfileImageModleForm(forms.ModelForm):
    pass
