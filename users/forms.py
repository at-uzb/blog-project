from .models import User
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Parolni takrorlang",
                                 widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','email']
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""
    
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("Parolingiz bir biriga mos kelmadi!")
        return data['password2']
    
    
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']




    
