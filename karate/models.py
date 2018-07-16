from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
contact = RegexValidator(r"[0-9]{10}", "Enter a valid mobile number without country code example:5199816450 (length must be 10)")

# Create your models here.


class Student(models.Model):
    RANK_CHOICES = [
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
        ('HALF GREEN', 'HALF GREEN'),
        ('GREEN', 'GREEN'),
        ('HALF BLUE', 'HALF BLUE'),
        ('BLUE', 'BLUE'),
        ('HALF RED', 'HALF RED'),
        ('RED', 'RED'),
        ('HALF BLACK', 'HALF BLACK'),
        ('BLACK', 'BLACK')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    mobile = models.CharField(max_length=10, validators=[contact])
    email = models.EmailField()
    street_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    is_parent = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    parent_for = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    rank = models.CharField(max_length=12, choices=RANK_CHOICES, default="WHITE")

    def __str__(self):
        return self.first_name

class Parent(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=10, validators=[contact])
    email = models.EmailField()
    street_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Class(models.Model):
    levels = [
        ('BG', 'Beginner'),
        ('IM', 'Intermediate'),
        ('AD', 'Advanced'),
    ]

    days = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]

    class_id = models.CharField(max_length=4, unique=True)
    class_level = models.CharField(max_length=2, choices=levels, default='BG')
    class_timing = models.TimeField()
    class_day = models.CharField(max_length=3, choices=days, default='MONDAY')

    def __str__(self):
        return self.class_id


class Attendance(models.Model):
    date_taken = models.DateField(default=timezone.now)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.classroom.class_id


class Progress(models.Model):
    ranks = [
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
        ('HALF GREEN', 'HALF GREEN'),
        ('GREEN', 'GREEN'),
        ('HALF BLUE', 'HALF BLUE'),
        ('BLUE', 'BLUE'),
        ('HALF RED', 'HALF RED'),
        ('RED', 'RED'),
        ('HALF BLACK', 'HALF BLACK'),
        ('BLACK', 'BLACK'),
    ]

    rank = models.CharField(max_length=15, choices=ranks, default='WHITE')
    date_achieved = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.rank + " - " + self.student.first_name + " " + self.student.last_name


class Payment(models.Model):
    fee_category = [
        ('MS', 'Membership'),
        ('TE', 'Test'),
        ('PP', 'Product Purchase'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=2, choices=fee_category, default='MS')
    payment_date = models.DateField(default=timezone.now)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.student.first_name + "/" + self.fee_type + "-" + str(self.payment_date)


class GuestStudent(models.Model):
    RANK_CHOICES = [
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
        ('HALF GREEN', 'HALF GREEN'),
        ('GREEN', 'GREEN'),
        ('HALF BLUE', 'HALF BLUE'),
        ('BLUE', 'BLUE'),
        ('HALF RED', 'HALF RED'),
        ('RED', 'RED'),
        ('HALF BLACK', 'HALF BLACK'),
        ('BLACK', 'BLACK')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    mobile = models.CharField(max_length=10, validators=[contact])
    email = models.EmailField()
    street_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    is_parent = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    parent_for = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    rank = models.CharField(max_length=12, choices=RANK_CHOICES, default="WHITE")

    def __str__(self):
        return self.first_name


class GuestParent(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=10, validators=[contact])
    email = models.EmailField()
    street_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    student = models.ForeignKey(GuestStudent, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name


class GuestClass(models.Model):
    levels = [
        ('BG', 'Beginner'),
        ('IM', 'Intermediate'),
        ('AD', 'Advanced'),
    ]

    days = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]

    class_id = models.CharField(max_length=4, unique=True)
    class_level = models.CharField(max_length=2, choices=levels, default='BG')
    class_timing = models.TimeField()
    class_day = models.CharField(max_length=3, choices=days, default='MON')

    def __str__(self):
        return self.class_id


class GuestAttendance(models.Model):
    date_taken = models.DateField(default=timezone.now)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(GuestStudent, on_delete=models.CASCADE)

    def __str__(self):
        return self.classroom.class_id


class GuestProgress(models.Model):
    ranks = [
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
        ('HALF GREEN', 'HALF GREEN'),
        ('GREEN', 'GREEN'),
        ('HALF BLUE', 'HALF BLUE'),
        ('BLUE', 'BLUE'),
        ('HALF RED', 'HALF RED'),
        ('RED', 'RED'),
        ('HALF BLACK', 'HALF BLACK'),
        ('BLACK', 'BLACK'),
    ]

    rank = models.CharField(max_length=15, choices=ranks, default='WHITE')
    date_achieved = models.DateField(default=timezone.now)
    student = models.ForeignKey(GuestStudent, on_delete=models.CASCADE)

    def __str__(self):
        return self.rank + " - " + self.student.first_name + " " + self.student.last_name


class GuestPayment(models.Model):
    fee_category = [
        ('MS', 'Membership'),
        ('TE', 'Test'),
        ('PP', 'Product Purchase'),
    ]

    student = models.ForeignKey(GuestStudent, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=2, choices=fee_category, default='MS')
    payment_date = models.DateField(default=timezone.now)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.student.first_name + "/" + self.fee_type + "-" + str(self.payment_date)