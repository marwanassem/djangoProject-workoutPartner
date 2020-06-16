from django import forms
from tracker.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Lifter

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1', 'password2',
        ]


class LifterAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Lifter
        fields = ['username', 'password']

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid credentials")


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['Name']


class WorkoutEditForm(forms.ModelForm):
    # Workout = forms.CharField(widget=forms.Textarea)
    # Exc     = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = WorkoutExercise
        # widgets = {
        #     'exercise.ExcName': forms.Textarea()
        # }
        # fields = ['Name', 'exercise']#'ExcName', 'set_reps', 'Note']
        fields = '__all__'


class MuscleForm(forms.ModelForm):
    Name = forms.CharField(max_length=100, label='Muscle',
                           help_text='Choose a muscle group to explore exercises')

    class Meta:
        model = MuscleGroup
        fields = ['Name', ]


class ExerciseToWorkout(forms.ModelForm):
    ExcName = forms.CharField(max_length=100, label='Exercise Name', help_text='Exercise Name is required.')
    set_reps = forms.CharField(max_length=500, label='# Sets and Reps',
                               help_text='Add each set of your exercise and its reps',
                               widget=forms.Textarea())

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


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['ExcName', ]


class ExerciseBuildingForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['weight', 'set_reps', 'Note', ]


class EditExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['weight', 'set_reps', 'Note',]


class DeleteExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = []
