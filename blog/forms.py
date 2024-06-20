from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from blog.models import Comment


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'inputUserName',
                                       'type': 'username',
                                       'placeholder': 'Enter your name'
                                   }
                               ))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'inputPassword',
                                   'type': 'password',
                                   'placeholder': 'Password'
                               }))
    password2 = forms.CharField(label='Confirm password', required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'ReInputPassword',
                                   'type': 'password',
                                   'placeholder': 'Repeat Password'
                               }))

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Passwords are different. Please confirm password again')

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'])
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('User with such username has already exists. Please enter different username.')
        return username


class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'inputUserName',
                                       'type': 'username',
                                       'placeholder': 'Enter your name'
                                   }
                               ))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'inputPassword',
                                   'type': 'password',
                                   'placeholder': 'Password'
                               }))


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=100,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'id': 'name',
                                   'placeholder': 'Your name'
                               }
                           ))
    email = forms.CharField(required=True, max_length=100,
                           widget=forms.EmailInput(
                               attrs={
                                   'class': 'form-control',
                                   'id': 'email',
                                   'placeholder': 'Your e-mail'
                               }
                           ))
    subject = forms.CharField(required=True, max_length=200,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'id': 'subject',
                                   'placeholder': 'Subject'
                               }
                           ))
    message = forms.CharField(required=True, max_length=200,
                              widget=forms.Textarea(
                                  attrs={
                                      'class': 'form-control md-textarea',
                                      'id': 'message',
                                      'placeholder': 'Message',
                                      'rows': 3
                                  }
                              ))


class CommentForm(forms.ModelForm):
    text = forms.CharField(min_length=10, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control mb-3', 'rows': 3})
                           )

    class Meta:
        model = Comment
        fields = ('text', )
