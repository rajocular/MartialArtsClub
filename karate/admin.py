from django.contrib import admin
from karate.forms import GuestAdminStudentForm
from .models import Student, Parent, Class, Attendance, Payment, Progress
from .models import GuestStudent, GuestParent, GuestClass, GuestAttendance, GuestPayment, GuestProgress
# Register your models here.


class GuestStudentAdmin(admin.ModelAdmin):
    form = GuestAdminStudentForm


admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(Payment)
admin.site.register(Progress)

admin.site.register(GuestStudent, GuestStudentAdmin)
admin.site.register(GuestParent)
admin.site.register(GuestClass)
admin.site.register(GuestAttendance)
admin.site.register(GuestPayment)
admin.site.register(GuestProgress)