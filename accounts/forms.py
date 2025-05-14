from django import forms
from .models import Profile, Skill

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'user_type', 'skills']  # Ensure 'skills' is included here
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'user_type': forms.Select(choices=Profile.USER_TYPES),
            'skills': forms.CheckboxSelectMultiple(),  # Use Checkboxes to select multiple skills
        }

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),  # Ensure all skills are displayed
        widget=forms.CheckboxSelectMultiple(),  # Checkboxes allow selection of multiple skills
        required=False  # Make this field optional
    )
