from django import forms
from karate.models import Student, Parent, Class, Attendance, Progress, Payment
from karate.models import GuestStudent, GuestParent, GuestClass, GuestAttendance, GuestPayment, GuestProgress


class StudentForm(forms.ModelForm):
    class Meta:
        model = GuestStudent
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_joined', 'mobile', 'email', 'street_name', 'city', 'province', 'is_parent', 'parent_for' )


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_joined', 'mobile', 'email', 'street_name', 'city', 'province', 'is_parent', 'rank', 'parent_for')

    def clean(self):
        if self.cleaned_data['is_parent'] == 'No' and self.cleaned_data['parent_for']:
            raise forms.ValidationError("You cannot choose parent_for if you are not the parent")
        if self.cleaned_data['is_parent'] == 'Yes' and self.cleaned_data['parent_for']:
            raise forms.ValidationError("You must a choose a student as you have given 'Yes' for is_parent field")
        if self.cleaned_data['is_parent'] == 'Yes'and self.cleaned_data['parent_for']:
            parent = Parent()
            parent.first_name = self.cleaned_data['first_name']
            parent.last_name = self.cleaned_data.get('last_name', '')
            parent.mobile = self.cleaned_data['mobile']
            parent.email = self.cleaned_data['email']
            parent.street_name = self.cleaned_data['street_name']
            parent.city = self.cleaned_data['city']
            parent.province = self.cleaned_data['province']
            parent.save()


class GuestStudentForm(forms.ModelForm):
    class Meta:
        model = GuestStudent
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_joined', 'mobile', 'email', 'street_name', 'city', 'province', 'is_parent', 'parent_for' )


class GuestAdminStudentForm(forms.ModelForm):
    class Meta:
        model = GuestStudent
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_joined', 'mobile', 'email', 'street_name', 'city', 'province', 'is_parent', 'rank', 'parent_for')

    def clean(self):
        if self.cleaned_data['is_parent'] == 'No' and self.cleaned_data['parent_for']:
            raise forms.ValidationError("'is_parent' field is set to 'No'.. You cannot choose parent_for")
        if self.cleaned_data['is_parent'] == 'Yes' and not self.cleaned_data['parent_for']:
            raise forms.ValidationError("'is_parent' field is set to 'Yes'.. You must a choose a student ")
        if self.cleaned_data['is_parent'] == 'Yes'and self.cleaned_data['parent_for']:
            parent = GuestParent()
            parent.first_name = self.cleaned_data['first_name']
            parent.last_name = self.cleaned_data.get('last_name', '')
            parent.mobile = self.cleaned_data['mobile']
            parent.email = self.cleaned_data['email']
            parent.street_name = self.cleaned_data['street_name']
            parent.city = self.cleaned_data['city']
            parent.province = self.cleaned_data['province']
            parent.student = self.cleaned_data['parent_for']
            parent.save()


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('first_name', 'last_name', 'mobile', 'email', 'street_name', 'city', 'province', 'student')


class GuestParentForm(forms.ModelForm):
    class Meta:
        model = GuestParent
        fields = ('first_name', 'last_name', 'mobile', 'email', 'street_name', 'city', 'province', 'student')


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('class_id', 'class_level', 'class_timing', 'class_day', )


class GuestClassForm(forms.ModelForm):
    class Meta:
        model = GuestClass
        fields = ('class_id', 'class_level', 'class_timing', 'class_day', )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date_taken', 'classroom', 'student',)


class GuestAttendanceForm(forms.ModelForm):
    class Meta:
        model = GuestAttendance
        fields = ('date_taken', 'classroom', 'student',)


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ('rank', 'date_achieved', 'student',)


class GuestProgressForm(forms.ModelForm):
    class Meta:
        model = GuestProgress
        fields = ('rank', 'date_achieved', 'student',)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('student', 'fee_type', 'payment_date', 'amount')


class GuestPaymentForm(forms.ModelForm):
    class Meta:
        model = GuestPayment
        fields = ('student', 'fee_type', 'payment_date', 'amount')