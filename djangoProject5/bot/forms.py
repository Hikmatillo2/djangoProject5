from django import forms
from .models import ParentButton
from .models import Admin
from .models import ChildButton
from .models import GrandParentButton


class GrandParentForm(forms.ModelForm):
    class Meta:
        model = GrandParentButton
        fields = ('name', 'text', 'attachment')
        widgets = {
            'name': forms.TextInput,
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = ParentButton
        fields = ('grandparent', 'name', 'text', 'attachment')
        widgets = {
            'name': forms.TextInput,
        }


class ChildForm(forms.ModelForm):
    class Meta:
        model = ChildButton
        fields = ('parent', 'name', 'text', 'attachment')
        widgets = {
            'name': forms.TextInput,
        }


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('id', 'firts_name', 'last_name', 'mail')
        widgets = {
            'id': forms.TextInput,
            'firts_name': forms.TextInput,
            'last_name': forms.TextInput,
            'mail': forms.TextInput
        }


