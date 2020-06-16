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


class AboutView(TemplateView):
    template_name = 'about.html'


class WorkoutListView(ListView):
    model = Workout
    template_name = 'workout/workout_list.html'

    def get_queryset(self):
        return Workout.objects.filter(is_published=True)


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'workout/workout_edit.html'
    form_class = WorkoutEditForm
    model = Workout

    def get_success_url(self):
        return reverse(viewname='home')

    def form_invalid(self, form):
        print(form.fields)


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = 'workout/confirm_delete.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return get_object_or_404(Workout, id=pk)

    def get_success_url(self):
        return reverse(viewname='home')


class MuscleListView(ListView):
    model = MuscleGroup
    template_name = 'muscle/muscles_list.html'

    def get_queryset(self):
        return MuscleGroup.objects.all()

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
                Creator=lifter
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
        workout.is_published = True
        workout.save()
        return redirect('home')

    if request.method == 'POST' and request.POST.get('add_exercise') == '':
        add_exercise(request, id)

    context = {
        'Workout': workout,
        'form': form
    }

    return render(request, 'workout/add_to_workout.html', context)


@login_required
def new_workout(request):

    lifter = Lifter.objects.get(id=request.user.id)
    workout_form = WorkoutForm()
    workout = None

    if request.POST.get("start") == '':
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            workout = workout_form.save(commit=False)
            workout.Creator = lifter
            workout.save()
            return redirect('working', w_id=workout.pk)

    return render(request, 'workout/workout_form.html', {'workout_form': workout_form})


@login_required
def workout_detail(request, id):
    workout = get_object_or_404(Workout, id=id)
    context = {
        'workout':workout,
    }
    return render(request, 'workout/workout_detail.html', context=context)


@login_required
def edit_exercise(request, id, id2):
    workout = get_object_or_404(Workout, id=id)
    exc = get_object_or_404(Exercise, id=id2)

    if request.method == 'POST':
        form = EditExerciseForm(request.POST)
        if form.is_valid():
            exc.weight = form.cleaned_data['weight']
            exc.set_reps = form.cleaned_data['set_reps']
            exc.Note = form.cleaned_data['Note']
            exc.save()
            workout.save()
            return redirect('workout_detail', id=id)
        else:
            form = EditExerciseForm()
    else:
        form = EditExerciseForm()
    return render(request, 'exercise/edit_exercise.html', {'form':form})


@login_required
def delete_exercise(request, id, id2):
    workout = get_object_or_404(Workout, id=id)
    exc = get_object_or_404(Exercise, id=id2)
    form = DeleteExerciseForm()

    context = {
        'form': form,
        'obj': exc,
    }

    if request.method == 'POST':
        exc.delete()
        workout.save()

        return redirect('workout_detail', id=id)

    return render(request, 'exercise/del_exercise.html', context=context)


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


def register_lifter(request):
    context = {}
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            lifter = authenticate(username=username, password=password)
            login(request, user=lifter)
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = SignUpForm()
        context['form'] = form

    return render(request, 'registration/register.html', context=context)


def login_lifter(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LifterAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LifterAuthenticationForm()

    context['login_form'] = form

    return render(request, 'registration/login.html', context=context)


def temp_view(request):
    return HttpResponse('Go to /accounts please')


def retrieve_muscle(request, w_id):
    form = MuscleForm()
    workout = get_object_or_404(Workout, id=w_id)
    name = None
    id = ''

    if request.method == 'POST' and request.POST.get("publish_workout") == '':
        workout.publish_workout()
        return redirect('home')

    if request.method == 'POST':
        form = MuscleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            muscle = MuscleGroup.objects.all()

            for m in muscle:
                if m.Name == name:
                    id = m.pk
                    break

            if id is None:
                return HttpResponse("Not found")

            return redirect('muscle_exc', w_id=w_id, muscle_id=id)

    form = MuscleForm()
    context = {
        'muscle_form': form,
        'workout': workout,
    }
    return render(request, 'workout/build_workout.html', context=context)


def retrieve_exercises(request, w_id, muscle_id):
    print('retrieving exercises')
    workout = get_object_or_404(Workout, pk=w_id)
    muscle = MuscleGroup.objects.get(pk=muscle_id)
    exc_list = Exercise.return_exercises(Exercise, muscle)
    form = ExerciseForm()

    context = {
        'muscle': muscle,
        'objects': exc_list,
        'w_id': workout.pk,
        'exc_form': form,
    }

    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            creator = request.user
            exc_name = form.cleaned_data['ExcName']

            new_exercise = Exercise.objects.create(
                ExcName=exc_name,
                Creator=creator,
                muscle=muscle,
            )

            new_exercise.save()
            workout.exercise.add(new_exercise)
            workout.save()
            return redirect('build_workout', w_id=w_id, e_id=new_exercise.pk)
    else:
        print(request.POST)

    return render(request, 'muscle/muscle_exercises.html', context=context)


def handle_adding_workout(request, w_id, e_id):
    form = ExerciseBuildingForm()
    muscle_form = MuscleForm()
    workout = get_object_or_404(Workout, id=w_id)
    exercise = get_object_or_404(Exercise, id=e_id)

    context = {
        'exercise_form': form,
        'workout': workout,
        'muscle_form': muscle_form,
        'received_exercise': exercise.ExcName,
    }
    print(request.POST)
    if request.method == 'POST' and request.POST.get("add_to_workout") == '':
        form = ExerciseBuildingForm(request.POST)
        if form.is_valid():
            print('valid form')
            exercise.weight = form.cleaned_data['weight']
            exercise.Note = form.cleaned_data['Note']
            exercise.set_reps = form.cleaned_data['set_reps']
            exercise.set_record.append(form.cleaned_data['set_reps'])
            exercise.weight_record.append(form.cleaned_data['weight'])
            exercise.save()
            workout.exercise.add(exercise)
            workout.save()
            return redirect('working', w_id=w_id)
        else:
            print(form.errors)
    elif request.method == 'POST' and request.POST.get("muscle_exercises") == '':
        return retrieve_muscle(request, workout.pk)
    elif request.method == 'POST' and request.POST.get("publish_workout") == '':
        workout.publish_workout()
        return redirect('home')
    else:
        form = ExerciseBuildingForm()
        context = {
            'exercise_form': form,
            'workout': workout,
            'muscle_form': muscle_form,
            'received_exercise': exercise.ExcName,
        }

    return render(request, 'workout/build_workout.html', context=context)


def retrieve_record(request, w_id, e_id):
    exercise = get_object_or_404(Exercise, id=e_id)
    set_record = exercise.set_record[len(exercise.set_record)-1]
    weight_record = exercise.weight_record[len(exercise.weight_record)-1]

    return HttpResponse('last record: ' + str(set_record))


@login_required
def workout_search(request):
    if request.method == 'POST':
        name = request.POST.get('workout_name', False)
        workout = Workout.objects.filter(Name=name).first()
        if not workout:
            return HttpResponse('Workout does not exist')
        return redirect('workout_detail', id=workout.pk)
    return render(request, 'base.html')