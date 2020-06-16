from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.register_lifter, name='register'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('workout/', views.WorkoutListView.as_view(), name='home'),
    # path('workout/<int:id>/working', views.adding_exercise_to_workout, name='adding_exercise_to_workout'),
    path('workout/<int:id>/', views.workout_detail, name='workout_detail'),
    path('workout/new/', views.new_workout, name='new_workout'),
    path('workout/<int:pk>/edit/', views.WorkoutUpdateView.as_view(), name='workout_edit'),
    path('workout/<int:pk>/remove/', views.WorkoutDeleteView.as_view(), name='workout_remove'),

    path('workout/<int:id>/edit-exc/<int:id2>/', views.edit_exercise, name='exercise_edit'),
    path('workout/<int:id>/del-exc/<int:id2>/', views.delete_exercise, name='exercise_delete'),

    path('workout/<int:w_id>/working/', views.retrieve_muscle, name='working'),

    path('muscle/<int:w_id>/m-exc/<int:muscle_id>/', views.retrieve_exercises, name='muscle_exc'),

    path('workout/<int:w_id>/working/<int:e_id>/adding/', views.handle_adding_workout, name='build_workout'),

    path('workout/<int:w_id>/working/<int:e_id>/rec/', views.retrieve_record, name='retrieve_record'),

    path('muscles/', views.MuscleListView.as_view(), name='muscles_list'),
    path('workout/search/', views.workout_search, name='workout_search'),
    # path('workout/<int:id>/working/<int:e_id>/', views, name='')


    # path('muscle/new/', views.CreateMuscleGroupView.as_view(), name='new_muscle'),
    # path('exercise/new/<int:id>/', views.add_exercise, name='new_exercise'),
    # re_path(r'workout/(?P<pk>\d+)/exercise/$', views.add_exercise_to_workout, name='add_exercise_to_workout'),
    # re_path(r'workout/(?P<pk>\d+)/remove_exercise_workout/$', views.remove_exercise_from_workout, name='remove_exercise_from_workout'),
    # re_path(r'workout/(?P<pk>\d+)/publish_workout/$', views.publish_workout, name='workout_publish'),
    # re_path(r'exercise/(?P<pk>\d+)/remove_exercise/$', views.delete_exercise, name='exercise_remove'),

]
