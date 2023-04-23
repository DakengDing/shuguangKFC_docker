from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Renwu


class SignUpForm(UserCreationForm):
    #qq = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'qq'}))
    #gameID = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'游戏角色名'}))



    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')




    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '用户名'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>必填！使用字母和数字组合 特殊字符只能使用 @/./+/-/_ </small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = '密码'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>密码至少为8位</li><li>不能为纯数字</li><li>密码不能太简单</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = '确认密码'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>重复上面的密码</small></span>'


class AddRenwu(forms.ModelForm):
    name = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder":"游戏角色名", "class":"form-control"}), label="")