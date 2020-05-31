from django import forms
from tracker.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Lifter

        fields = [
            'email',
            'first_name',
            'last_name',
            'username',
            'password1', 'password2',
            'gender', 'DOB'
        ]


class LifterAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Lifter
        fields = ['email', 'password']

        def clean(self):
            if self.is_valid():
                email = self.cleaned_data['email']
                password = self.cleaned_data['password']
                if not authenticate(email=email, password=password):
                    raise forms.ValidationError("Invalid credentials")


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['Name']


class WorkoutEditForm(forms.ModelForm):
    class Meta:
        model = Workout
        widgets = {
            'exercise.ExcName': forms.Textarea()
        }
        fields = ['Name', 'exercise']#'ExcName', 'set_reps', 'Note']


class MuscleForm(forms.ModelForm):
    class Meta:
        model = MuscleGroup
        fields = ['Name', ]


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['ExcName', 'muscle']


class ExerciseToWorkout(forms.ModelForm):
    class Meta:
        model = Exercise
        widgets = {
                'Note': forms.Textarea(),
                'set_reps': forms.Textarea(),

        }
        fields = ['ExcName', 'muscle', 'set_reps', 'Note']


class DeleteWorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('Name',)