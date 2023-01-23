from django import forms
from .models import Phrase

TOPIC_COUNTER = [(i, str(i)) for i in range(1, 11)]


class PhraseForm(forms.ModelForm):
    count = forms.TypedChoiceField(choices=TOPIC_COUNTER, coerce=int)

    class Meta:
        model = Phrase
        fields = ('category',)
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control form-control-lg'})
        }
        labels = {'category': ''}
