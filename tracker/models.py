from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class LifterAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        # if not gender:
        #     raise ValueError('Users must have a gender')
        # if not DOB:
        #     raise ValueError('Users must have a date of birth')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name,  password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Lifter(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    GENDER_CHOICES = (
                ('M', 'Male'),
                ('F', 'Female')
            )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name',]

    objects = LifterAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Workout(models.Model):
    Name = models.CharField(max_length=100)
    Creator = models.ForeignKey('Lifter', on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=timezone.now)
    exercise = models.ManyToManyField('Exercise', blank=True, null=True, through='WorkoutExercise')
    is_published = models.BooleanField(default=False)

    def add_workout(self):
        self.save()

    # def __str__(self):
    #     return "Workout: " + self.Name + " ,Created by: " + self.Creator.name


class MuscleGroup(models.Model):
    Name = models.CharField(max_length=100)

    def add_muscle_group(self):
        self.save()

    def __str__(self):
        return self.Name


class Exercise(models.Model):
    ExcName = models.CharField(max_length=100)
    muscle = models.ForeignKey('MuscleGroup', on_delete=models.PROTECT)
    set_reps = models.CharField(max_length=500, default=None, null=True, blank=True)
    Note = models.CharField(max_length=250, blank=True, null=True)

    def create_exercise(self):
        self.save()

    def __str__(self):
        return self.ExcName + " belongs to Muscle Group: " + self.muscle.Name


class Set(models.Model):
    reps = models.CharField(max_length=500)

    def __str__(self):
        return self.reps


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
