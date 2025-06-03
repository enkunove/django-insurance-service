from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "rate", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Напишите свой отзыв..."}),
            "rate": forms.Select(),
        }
