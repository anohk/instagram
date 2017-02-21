from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(max_length=60)


class PostForm(forms.Form):
    content = forms.CharField(required=False)
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )
