from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, DeleteView, UpdateView, ListView,
                                  DetailView, CreateView)
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from tracker.models import *
from tracker.forms import *

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


class AboutView(TemplateView):
    template_name = 'about.html'


class WorkoutListView(ListView):
    model = Workout
    template_name = 'workout/workout_list.html'

    def get_queryset(self):
        # return Workout.objects.filter(creation_date__lte=timezone.now()).order_by('-creation_date')
        return Workout.objects.filter(is_published = True)
        return Workout.objects.all()


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'workout/workout_edit.html'
    # redirect_field_name = 'tracker/workout/workout_detail.html'
    form_class = WorkoutEditForm
    model = Workout

    def get_success_url(self):
        return reverse(viewname='home')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = 'workout/confirm_delete.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Workout, id=pk)

    def get_success_url(self):
        return reverse(viewname='home')


class CreateMuscleGroupView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'muscle/muscles_detail.html'
    form_class = MuscleForm
    model = MuscleGroup


class CreateExerciseView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'exercise/exercise_form.html'
    #redirect_field_name = 'exercise/exercise_form.html'
    form_class = ExerciseToWorkout
    model = Exercise


@login_required
def add_exercise(request, id):
    lifter = Lifter.objects.get(id=request.user.id)
    if request.method == 'POST':
        print('**** Post ****')
        workout = get_object_or_404(Workout, id=id)
        form = ExerciseToWorkout(request.POST)
        if form.is_valid():
            print('**** Valid ****')
            exc_name = form.cleaned_data['ExcName']
            exc_muscle = form.cleaned_data['muscle']
            exc_set_reps = form.cleaned_data['set_reps']
            exc_note = form.cleaned_data['Note']
            exc_saved = Exercise.objects.create(
                ExcName=exc_name,
                muscle=exc_muscle,
                set_reps=exc_set_reps,
                Note=exc_note,
            )
            exc_saved.save()

            workout.exercise.add(exc_saved)
            return redirect('adding_exercise_to_workout', id=id)
        else:
            print(form.errors)
            print('**** Not Valid ****')
            return render(request, 'exercise/exercise_form.html', {'form': form})
    else:
        print('**** Not Post ****')
        form = ExerciseToWorkout()

    return render(request, 'exercise/exercise_form.html', {'form': form})


@login_required
def adding_exercise_to_workout(request, id):
    workout = get_object_or_404(Workout, id=id)
    form = ExerciseToWorkout()

    if request.POST.get('publish_workout') == '':
        print('**** Publishing Workout ****')
        workout.is_published = True
        workout.save()
        return redirect('home')

    if request.method == 'POST' and request.POST.get('add_exercise') == '':
        add_exercise(request, id)

    context = {
        'Workout': workout,
        'form': form
    }

    print(request.POST)

    return render(request, 'workout/add_to_workout.html', context)


@login_required
def new_workout(request):

    lifter = Lifter.objects.get(id=request.user.id)
    workout_form = WorkoutForm()
    workout = None

    if request.POST.get("add_exercise") == '':

        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            print('**** Valid Workout form ****')

            workout = workout_form.save(commit=False)
            print(workout.pk)
            workout.Creator = lifter
            workout.save()
            print(workout.pk)
            # lifter.workouts.add(workout)
            return redirect('adding_exercise_to_workout', id=workout.pk)
        else:
            print('**** Not Valid Workout form ****')

    if request.method == "POST":
        if workout_form.is_valid():
            workout.save()
            return redirect('workout_detail')
        else:
            print(workout_form.errors)
            return render(request, 'workout/workout_form.html', {'workout_form': workout_form})

    else:
        return render(request, 'workout/workout_form.html', {'workout_form':workout_form})


@login_required
def workout_detail(request, id):
    workout = get_object_or_404(Workout, id=id)

    context = {
        'workout':workout,
    }
    return render(request, 'workout/workout_detail.html', context=context)


@login_required
def delete_workout(request, id):
    form = DeleteWorkoutForm()
    obj = get_object_or_404(Workout, id=id)
    context = {
        'form': form,
        'obj': obj
    }
    if request.method == 'POST':
        # form = DeleteWorkoutForm(request.POST)
        obj.delete()
        return redirect('home')
    else:
        return render(request, 'workout/confirm_delete.html', context=context)

@login_required
def add_exercise_to_workout(request, id):
    workout = get_object_or_404(Workout, id=id)
    if request.method == 'POST':
        form = ExerciseToWorkout(request.POST)
        if form.is_valid():
            exc = form.save(commit=True)
            exc.save()
            return redirect('workout/workout_detail.html', id=id)
    else:
        form = ExerciseForm

    return render(request, 'tracker/exercise/exercise_to_workout.html')


@login_required
def remove_exercise_from_workout(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    workout_pk = exercise.workout.pk
    # Need to check whether it deletes the exc from only the workout or from the whole DB.
    exercise.delete()
    return redirect('workout/workout_detail.html', pk=workout_pk)


@login_required
def publish_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    workout.add_workout()
    return redirect('workout/workout_detail.html', pk=pk)


@login_required
def edit_workout(request):
    pass


@login_required
def delete_workout(request):
    pass


@login_required
def delete_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    muscle_pk = exercise.muscle.pk
    exercise.delete()
    redirect('muscle/muscle_detail.html', pk=muscle_pk)


def register_lifter(request):
    context = {}
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            lifter = authenticate(email=email, password=password)
            login(request, lifter)
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = SignUpForm()
        context['form'] = form

    return render(request, 'registration/register.html', context=context)


def login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LifterAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = LifterAuthenticationForm()

    context['login_form'] = form

    return render(request, 'registration/login.html', context)


def temp_view(request):
    return HttpResponse('Go to /accounts please')