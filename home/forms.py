from django import forms

from .models import Post, GoTender, BuyTender

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
                'compania',
                'inn',
                'kpp',
                'phone',
                'title',
                'text',
                'cost',
                'que',
                'region',
                'supply',
                'start',
                'ending',
                'nameFile'
                  )
        widgets = {
            'start': forms.DateInput(attrs={'class': 'datetime-input'}),
            'ending': forms.DateInput(attrs={'class': 'datetime-input'})
        }
class CashForm(forms.ModelForm):
    #tenders = forms.ModelChoiceField(queryset=Post.objects.all())
    class Meta:
        model = GoTender
        fields = (
            'cash',
            'ques',
            'phones',
            #'tenders'
        )

class BuyForm(forms.ModelForm):
    class Meta:
        model = BuyTender
        fields = (
            #'tenders',
            #'client',
            )

from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #chek = forms.BooleanField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        #user.chek = self.cleaned_data['chek']

        if commit:
            user.save()
        return user