from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    """
    Form for adding new shopping items.
    """
    class Meta:
        model = Item
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'What to add?',
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control',
                'style': 'width: 100px;',
            }),
        }
