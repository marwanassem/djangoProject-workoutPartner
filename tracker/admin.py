from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Lifter, AccountAdmin)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)
admin.site.register(MuscleGroup)
admin.site.register(WorkoutExercise)
