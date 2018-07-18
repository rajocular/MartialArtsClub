from .models import Student, Parent, Class, Attendance, Progress, Payment
from .models import GuestStudent, GuestParent, GuestClass, GuestAttendance, GuestPayment, GuestProgress
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from karate.forms import StudentForm, ParentForm, ClassForm, AttendanceForm, ProgressForm, PaymentForm
from karate.forms import GuestAttendanceForm, GuestClassForm, GuestParentForm, GuestPaymentForm, GuestProgressForm, GuestStudentForm
from django.contrib.auth.forms import PasswordChangeForm
import datetime

# Create your views here.


def admin_home(request):
    return render(request, 'karate/home_page.html')


def guest_home(request):
    session_time = request.session.get('user_session', None)
    return render(request, 'karate/home_page.html', {'start_time': session_time})


def admin_login(request):
    logout(request)
    start_date = (datetime.datetime.now() + datetime.timedelta(hours=-4)).strftime("%b %d, %Y %H:%M:%S")
    request.session['user_session'] = str(start_date)
    request.session.set_expiry(1800)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('karate:admin_home'))
        else:
            return render(request, 'karate/login_error.html')
    else:
        return render(request, 'karate/admin_login.html')


def session_expired(request):
    GuestStudent.objects.all().delete()
    GuestParent.objects.all().delete()
    GuestClass.objects.all().delete()
    GuestAttendance.objects.all().delete()
    GuestProgress.objects.all().delete()
    GuestPayment.objects.all().delete()
    return render(request, 'karate/session_expired.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'karate/password_change_done.html')
        else:
            return render(request, 'karate/password.html', {'form': form, 'code': 1})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'karate/password.html', {'form': form, 'code': 0})


@login_required
def admin_logout(request):
    logout(request)
    return render(request, 'karate/admin_logout.html')


def student_details(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        form_rank = ''
        if 'parent' in request.POST:
            is_p = request.POST['parent']
        if 'rank' in request.POST:
            rank = request.POST['rank']
        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                students = Student.objects.filter(first_name__icontains=search) | Student.objects.filter(last_name__icontains=search) | Student.objects.filter(email__icontains=search) | Student.objects.filter(street_name__icontains=search) | Student.objects.filter(city__icontains=search) | Student.objects.filter(province__icontains=search) | Student.objects.filter(rank__icontains=search) | Student.objects.filter(is_parent__icontains=search)
            else:
                students = GuestStudent.objects.filter(first_name__icontains=search) | GuestStudent.objects.filter(last_name__icontains=search) | GuestStudent.objects.filter(email__icontains=search) | GuestStudent.objects.filter(street_name__icontains=search) | GuestStudent.objects.filter(city__icontains=search) | GuestStudent.objects.filter(province__icontains=search) | GuestStudent.objects.filter(rank__icontains=search) | GuestStudent.objects.filter(is_parent__icontains=search)
            return render(request, 'karate/Student/student_details.html', {'students': students, 'query': search, 'start_time': session_time})
        elif 'date_factor' in request.POST:
            date_factor = request.POST['date_factor']
            if 'start_date' in request.POST:
                start_date = request.POST['start_date']
            if 'end_date' in request.POST:
                end_date = request.POST['end_date']
            if date_factor == "By date of birth":
                if request.user.is_authenticated:
                    students = Student.objects.filter(date_of_birth__range=(start_date, end_date))
                else:
                    students = GuestStudent.objects.filter(date_of_birth__range=(start_date, end_date))
            else:
                if request.user.is_authenticated:
                    students = Student.objects.filter(date_joined__range=(start_date, end_date))
                else:
                    students = GuestStudent.objects.filter(date_joined__range=(start_date, end_date))
            return render(request, 'karate/Student/student_details.html', {'students': students, 'start_time': session_time})
        elif 'sort_factor' in request.POST:
            sort_factor = request.POST['sort_factor']
            if 'sort_order' in request.POST:
                sort_order = request.POST['sort_order']
            if sort_order == 'Descending':
                if request.user.is_authenticated:
                    students = Student.objects.all().order_by('-'+sort_factor)
                else:
                    students = GuestStudent.objects.all().order_by('-' + sort_factor)
            else:
                if request.user.is_authenticated:
                    students = Student.objects.all().order_by(sort_factor)
                else:
                    students = GuestStudent.objects.all().order_by(sort_factor)
            return render(request, 'karate/Student/student_details.html', {'students': students, 'start_time': session_time})
        else:
            if rank == '--select--':
                if request.user.is_authenticated:
                    students = Student.objects.filter(is_parent=is_p)
                else:
                    students = GuestStudent.objects.filter(is_parent=is_p)
            else:
                if request.user.is_authenticated:
                    students = Student.objects.filter(is_parent=is_p, rank=rank)
                else:
                    students = GuestStudent.objects.filter(is_parent=is_p, rank=rank)
                form_rank += rank
            return render(request, 'karate/Student/student_details.html', {'students': students, 'form_parent': is_p, 'form_rank': form_rank, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            students = Student.objects.all()
        else:
            students = GuestStudent.objects.all()
        return render(request, 'karate/Student/student_details.html', {'students': students, 'form_parent': None, 'form_rank': None, 'start_time': session_time})


def parent_details(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                parents = Parent.objects.filter(first_name__icontains=search) | Parent.objects.filter(last_name__icontains=search) | Parent.objects.filter(email__icontains=search) | Parent.objects.filter(street_name__icontains=search) | Parent.objects.filter(city__icontains=search) | Parent.objects.filter(province__icontains=search) | Parent.objects.filter(student__first_name__icontains=search)
            else:
                parents = GuestParent.objects.filter(first_name__icontains=search) | GuestParent.objects.filter(last_name__icontains=search) | GuestParent.objects.filter(email__icontains=search) | GuestParent.objects.filter(street_name__icontains=search) | GuestParent.objects.filter(city__icontains=search) | GuestParent.objects.filter(province__icontains=search) | GuestParent.objects.filter(student__first_name__icontains=search)
            return render(request, 'karate/Parent/parent_details.html', {'parents': parents, 'query': search, 'start_time': session_time})
        elif 'sort_factor' in request.POST:
            sort_factor = request.POST['sort_factor']
            if 'sort_order' in request.POST:
                sort_order = request.POST['sort_order']

            if request.user.is_authenticated:
                parents = Parent.objects.all()
            else:
                parents = GuestParent.objects.all()
            if sort_order == 'Descending':
                parents = parents.order_by('-'+sort_factor)
            else:
                parents = parents.order_by(sort_factor)
            return render(request, 'karate/Parent/parent_details.html', {'parents': parents, 'sort': sort_factor + sort_order, 'start_time': session_time})
        else:
            if request.user.is_authenticated:
                parents = Parent.objects.all()
            else:
                parents = GuestParent.objects.all()
            return render(request, 'karate/Parent/parent_details.html', {'parents': parents, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            parents = Parent.objects.all()
        else:
            parents = GuestParent.objects.all()
        return render(request, 'karate/Parent/parent_details.html', {'parents': parents, 'start_time': session_time})


def class_details(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':

        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                classes = Class.objects.filter(class_id__icontains=search) | Class.objects.filter(class_level__icontains=search) | Class.objects.filter(class_day__icontains=search)
            else:
                classes = GuestClass.objects.filter(class_id__icontains=search) | GuestClass.objects.filter(class_level__icontains=search) | GuestClass.objects.filter(class_day__icontains=search)
            return render(request, 'karate/Class/class_details.html', {'classes': classes, 'query': search, 'start_time': session_time})
        elif 'sort_factor' in request.POST:
            sort_factor = request.POST['sort_factor']
            if request.user.is_authenticated:
                classes = Class.objects.all()
            else:
                classes = GuestClass.objects.all()
            if 'sort_order' in request.POST:
                sort_order = request.POST['sort_order']
            if sort_order == 'Descending':
                classes = classes.order_by('-' + sort_factor)
            else:
                classes = classes.order_by(sort_factor)
            return render(request, 'karate/Class/class_details.html',
                          {'classes': classes, 'sort': sort_factor + sort_order, 'start_time': session_time})
        else:
            if request.user.is_authenticated:
                classes = Class.objects.all()
            else:
                classes = GuestClass.objects.all()
            return render(request, 'karate/Class/class_details.html', {'classes': classes, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            classes = Class.objects.all()
        else:
            classes = GuestClass.objects.all()
        return render(request, 'karate/Class/class_details.html', {'classes': classes, 'start_time': session_time})


def attendance_details(request):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        records = Attendance.objects.all()
    else:
        records = GuestAttendance.objects.all()
    if request.method == 'POST':

        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                records = Attendance.objects.filter(student__first_name__contains=search) | Attendance.objects.filter(student__last_name__icontains=search) | Attendance.objects.filter(student__email__icontains=search) | Attendance.objects.filter(student__street_name__icontains=search) | Attendance.objects.filter(student__city__icontains=search) | Attendance.objects.filter(student__province__icontains=search) | Attendance.objects.filter(student__rank__icontains=search) | Attendance.objects.filter(student__is_parent__icontains=search) | Attendance.objects.filter(classroom__class_id__icontains=search[0])
            else:
                records = GuestAttendance.objects.filter(student__first_name__contains=search) | GuestAttendance.objects.filter(student__last_name__icontains=search) | GuestAttendance.objects.filter(student__email__icontains=search) | GuestAttendance.objects.filter(student__street_name__icontains=search) | GuestAttendance.objects.filter(student__city__icontains=search) | GuestAttendance.objects.filter(student__province__icontains=search) | GuestAttendance.objects.filter(student__rank__icontains=search) | GuestAttendance.objects.filter(student__is_parent__icontains=search) | GuestAttendance.objects.filter(classroom__class_id__icontains=search[0])
            return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'start_time': session_time})
        elif 'rank' in request.POST:
            rank = request.POST['rank']
            if request.user.is_authenticated:
                records = Attendance.objects.filter(classroom__class_id__contains=rank[0])
            else:
                records = GuestAttendance.objects.filter(classroom__class_id__contains=rank[0])
            return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'query': rank, 'start_time': session_time})
        elif 'start_date' in request.POST:
            start_date = request.POST['start_date']
            if 'end_date' in request.POST:
                end_date = request.POST['end_date']
            if request.user.is_authenticated:
                records = Attendance.objects.filter(date_taken__range=(start_date, end_date))
            else:
                records = GuestAttendance.objects.filter(date_taken__range=(start_date, end_date))
            return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'start_time': session_time})
        elif 'sort_order' in request.POST:
            sort_order = request.POST['sort_order']
            if sort_order == 'Descending':
                records = records.order_by('-date_taken')
            else:
                records = records.order_by('date_taken')
            return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'start_time': session_time})
        else:
            return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'start_time': session_time})
    else:
        return render(request, 'karate/Attendance/attendance_details.html', {'records': records, 'start_time': session_time})


def progress_details(request):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        records = Progress.objects.all()
    else:
        records = GuestProgress.objects.all()
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                records = Progress.objects.filter(student__first_name__icontains=search) | Progress.objects.filter(student__last_name__icontains=search) | Progress.objects.filter(student__email__icontains=search) | Progress.objects.filter(student__street_name__icontains=search) | Progress.objects.filter(student__city__icontains=search) | Progress.objects.filter(student__province__icontains=search) | Progress.objects.filter(student__rank__icontains=search) | Progress.objects.filter(student__is_parent__icontains=search)
            else:
                records = GuestProgress.objects.filter(student__first_name__icontains=search) | GuestProgress.objects.filter(student__last_name__icontains=search) | GuestProgress.objects.filter(student__email__icontains=search) | GuestProgress.objects.filter(student__street_name__icontains=search) | GuestProgress.objects.filter(student__city__icontains=search) | GuestProgress.objects.filter(student__province__icontains=search) | GuestProgress.objects.filter(student__rank__icontains=search) | GuestProgress.objects.filter(student__is_parent__icontains=search)
            return render(request, 'karate/Progress/progress_details.html', {'records': records, 'start_time': session_time})
        elif 'rank' in request.POST:
            rank = request.POST['rank']
            if request.user.is_authenticated:
                records = Progress.objects.filter(rank=rank)
            else:
                records = GuestProgress.objects.filter(rank=rank)
            return render(request, 'karate/Progress/progress_details.html', {'records': records, 'query': rank, 'start_time': session_time})
        elif 'start_date' in request.POST:
            start_date = request.POST['start_date']
            if 'end_date' in request.POST:
                end_date = request.POST['end_date']
            if request.user.is_authenticated:
                records = Progress.objects.filter(date_achieved__range=(start_date, end_date))
            else:
                records = GuestProgress.objects.filter(date_achieved__range=(start_date, end_date))
            return render(request, 'karate/Progress/progress_details.html', {'records': records, 'start_time': session_time})
        elif 'sort_order' in request.POST:
            sort_order = request.POST['sort_order']
            if sort_order == 'Descending':
                records = records.order_by('-date_achieved')
            else:
                records = records.order_by('date_achieved')
            return render(request, 'karate/Progress/progress_details.html', {'records': records, 'start_time': session_time})
        else:
            return render(request, 'karate/Progress/progress_details.html', {'records': records, 'start_time': session_time})
    else:
        return render(request, 'karate/Progress/progress_details.html', {'records': records, 'start_time': session_time})


def payment_details(request):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        records = Payment.objects.all()
    else:
        records = GuestPayment.objects.all()
    if request.method == 'POST':
        if 'fee_type' in request.POST:
            fee_type = request.POST['fee_type']
            if request.user.is_authenticated:
                records = Payment.objects.filter(fee_type=fee_type)
            else:
                records = GuestPayment.objects.filter(fee_type=fee_type)
            return render(request, 'karate/Payment/payment_details.html', {'records': records, 'start_time': session_time})
        if 'search' in request.POST:
            search = request.POST['search']
            if request.user.is_authenticated:
                records = Payment.objects.filter(student__first_name__icontains=search) | Payment.objects.filter(student__last_name__icontains=search) | Payment.objects.filter(student__email__icontains=search) | Payment.objects.filter(student__street_name__icontains=search) | Payment.objects.filter(student__city__icontains=search) | Payment.objects.filter(student__province__icontains=search) | Payment.objects.filter(student__rank__icontains=search) | Payment.objects.filter(student__is_parent__icontains=search) | Payment.objects.filter(fee_type__icontains=search[0] )
            else:
                records = GuestPayment.objects.filter(student__first_name__icontains=search) | GuestPayment.objects.filter(student__last_name__icontains=search) | GuestPayment.objects.filter(student__email__icontains=search) | GuestPayment.objects.filter(student__street_name__icontains=search) | GuestPayment.objects.filter(student__city__icontains=search) | GuestPayment.objects.filter(student__province__icontains=search) | GuestPayment.objects.filter(student__rank__icontains=search) | GuestPayment.objects.filter(student__is_parent__icontains=search) | GuestPayment.objects.filter(fee_type__icontains=search[0])
            return render(request, 'karate/Payment/payment_details.html', {'records': records, 'query': search, 'start_time': session_time})
        elif 'start_date' in request.POST:
            start_date = request.POST['start_date']
            if 'end_date' in request.POST:
                end_date = request.POST['end_date']
            if request.user.is_authenticated:
                records = Payment.objects.filter(payment_date__range=(start_date, end_date))
            else:
                records = GuestPayment.objects.filter(payment_date__range=(start_date, end_date))
            return render(request, 'karate/Payment/payment_details.html', {'records': records, 'start_time': session_time})
        elif 'sort_factor' in request.POST:
            sort_factor = request.POST['sort_factor']
            if 'sort_order' in request.POST:
                sort_order = request.POST['sort_order']
            if sort_order == 'Descending':
                if sort_factor == 'Date':
                    records = records.order_by('-payment_date')
                elif sort_factor == 'amount':
                    records = records.order_by('-amount')
                else:
                    records = records.order_by('-student__'+sort_factor)
            else:
                if sort_factor == 'Date':
                    records = records.order_by('payment_date')
                elif sort_factor == 'amount':
                    records = records.order_by('amount')
                else:
                    records = records.order_by('student__'+sort_factor)
            return render(request, 'karate/Payment/payment_details.html', {'records': records, 'start_time': session_time})
        else:
            return render(request, 'karate/Payment/payment_details.html', {'records': records, 'start_time': session_time})
    else:
        return render(request, 'karate/Payment/payment_details.html', {'records': records, 'form_parent': None, 'form_rank': None, 'start_time': session_time})


def student_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = StudentForm(request.POST)
        else:
            form = GuestStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.rank = 'WHITE'
            # if student.is_parent == 'Yes' and student.parent_for is None:
            #     msg = '"is_parent" field is set to "Yes", You must a choose a student '
            #     return render(request, 'karate/Student/student_register.html', {'form': form, 'msg': msg})
            # if student.is_parent == 'No' and student.parent_for:
            #     msg = '"is_parent" field is set to "No", You cannot choose parent_for '
            #     return render(request, 'karate/Student/student_register.html', {'form': form, 'msg': msg})
            student.save()
            if student.is_parent == 'Yes':
                if request.user.is_authenticated:
                    parent = ParentForm(request.POST)
                else:
                    parent = GuestParentForm(request.POST)
                parent.first_name = student.first_name
                parent.last_name = student.last_name
                parent.mobile = student.mobile
                parent.email = student.email
                parent.street_name = student.street_name
                parent.city = student.city
                parent.province = student.province
                parent.save()
                if request.user.is_authenticated:
                    par = Parent.objects.latest('id')
                else:
                    par = GuestParent.objects.latest('id')
                return render(request, 'karate/Student/student_register_done.html', {'name': student.first_name + " " + student.last_name, 'parent_id': par.id, 'start_time': session_time})
            else:
                return render(request, 'karate/Student/student_register_done.html', {'name': student.first_name + " " + student.last_name, 'start_time': session_time})
        else:
            msg = 'You have entered Invalid details..Please enter proper values'
            # if request.user.is_authenticated:
            #     form = StudentForm()
            # else:
            #     form = GuestStudentForm()
            return render(request, 'karate/Student/student_register.html', {'form': form, 'msg': msg, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = StudentForm()
        else:
            form = GuestStudentForm()
        return render(request, 'karate/Student/student_register.html', {'form': form, 'start_time': session_time})


def parent_check(request, parent_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            parent_record = Parent.objects.get(id=parent_id)
            form = ParentForm(request.POST, instance=parent_record)
        else:
            parent_record = GuestParent.objects.get(id=parent_id)
            form = GuestParentForm(request.POST, instance=parent_record)
        if form.is_valid():
            parent = form.save(commit=False)

            if parent.student is None:
                return render(request, 'karate/Student/parent_check.html', {'error': "Note: You must select a student", 'form': form, 'start_time': session_time})
            else:
                parent.save()
                return render(request, 'karate/Student/parent_record_inserted.html', {'parent': parent.first_name, 'start_time': session_time})
        else:
            return render(request, 'karate/Student/parent_check.html', {'error': "Note: You must select a student", 'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            parent_record = Parent.objects.get(id=parent_id)
            form = ParentForm(instance=parent_record)
        else:
            parent_record = GuestParent.objects.get(id=parent_id)
            form = GuestParentForm(instance=parent_record)
        return render(request, 'karate/Student/parent_check.html', {'form': form, 'start_time': session_time})


def parent_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ParentForm(request.POST)
        else:
            form = GuestParentForm(request.POST)
        if form.is_valid():
            form.save()
            parent = form.save(commit=False)
            return render(request, 'karate/Parent/parent_register_done.html', {'name': parent.first_name + " " + parent.last_name, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ParentForm()
        else:
            form = GuestParentForm()
        return render(request, 'karate/Parent/parent_register.html', {'form': form, 'start_time': session_time})


def class_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ClassForm(request.POST)
        else:
            form = GuestClassForm(request.POST)
        if form.is_valid():
            form.save()
            class_form = form.save(commit=False)
            return render(request, 'karate/Class/class_register_done.html', {'name': class_form.class_id, 'start_time': session_time})
        else:
            return render(request, 'karate/Class/class_register_done.html', {'error': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ClassForm()
        else:
            form = GuestClassForm()
        return render(request, 'karate/Class/class_register.html', {'form': form, 'start_time': session_time})


def attendance_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AttendanceForm(request.POST)
        else:
            form = GuestAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            attendance_form = form.save(commit=False)
            return render(request, 'karate/Attendance/attendance_register_done.html', {'name': "Attendance taken on " + str(attendance_form.date_taken) + " for class", 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = AttendanceForm()
        else:
            form = GuestAttendanceForm()
        return render(request, 'karate/Attendance/attendance_register.html', {'form': form, 'start_time': session_time})


def progress_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ProgressForm(request.POST)
        else:
            form = GuestProgressForm(request.POST)
        if form.is_valid():
            form.save()
            progress_form = form.save(commit=False)
            return render(request, 'karate/Progress/progress_register_done.html', {'name': progress_form.student.first_name +'\'s', 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ProgressForm()
        else:
            form = GuestProgressForm()
        return render(request, 'karate/Progress/progress_register.html', {'form': form, 'start_time': session_time})


def payment_register(request):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PaymentForm(request.POST)
        else:
            form = GuestPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            payment_form = form.save(commit=False)
            return render(request, 'karate/Payment/payment_register_done.html', {'name': payment_form.student.first_name +'\'s', 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = PaymentForm()
        else:
            form = GuestPaymentForm()
        return render(request, 'karate/Payment/payment_register.html', {'form': form})


def student_edit(request, student_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        student = Student.objects.get(id=student_id)
    else:
        student = GuestStudent.objects.get(id=student_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = StudentForm(request.POST, instance=student)
        else:
            form = GuestStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Student/student_edit_done.html', {'form': form, 'student': student, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = StudentForm(instance=student)
        else:
            form = GuestStudentForm(instance=student)
        return render(request, 'karate/Student/student_edit.html', {'form': form, 'student': student, 'start_time': session_time})


def parent_edit(request, parent_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        parent = Parent.objects.get(id=parent_id)
    else:
        parent = GuestParent.objects.get(id=parent_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ParentForm(request.POST, instance=parent)
        else:
            form = GuestParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Parent/parent_edit_done.html', {'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ParentForm(instance=parent)
        else:
            form = GuestParentForm(instance=parent)
        return render(request, 'karate/Parent/parent_edit.html', {'form': form, 'parent': parent, 'start_time': session_time})


def class_edit(request, class_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        class_record = Class.objects.get(id=class_id)
    else:
        class_record = GuestClass.objects.get(id=class_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ClassForm(request.POST, instance=class_record)
        else:
            form = GuestClassForm(request.POST, instance=class_record)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Class/class_edit_done.html', {'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ClassForm(instance=class_record)
        else:
            form = GuestClassForm(instance=class_record)
        return render(request, 'karate/Class/class_edit.html', {'form': form, 'class_record': class_record, 'start_time': session_time})


def attendance_edit(request, attendance_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        attendance_record = Attendance.objects.get(id=attendance_id)
    else:
        attendance_record = GuestAttendance.objects.get(id=attendance_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AttendanceForm(request.POST, instance=attendance_record)
        else:
            form = GuestAttendanceForm(request.POST, instance=attendance_record)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Attendance/attendance_edit_done.html', {'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = AttendanceForm(instance=attendance_record)
        else:
            form = GuestAttendanceForm(instance=attendance_record)
        return render(request, 'karate/Attendance/attendance_edit.html', {'form': form, 'attendance_record': attendance_record, 'start_time': session_time})


def progress_edit(request, progress_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        progress_record = Progress.objects.get(id=progress_id)
    else:
        progress_record = GuestProgress.objects.get(id=progress_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ProgressForm(request.POST, instance=progress_record)
        else:
            form = GuestProgressForm(request.POST, instance=progress_record)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Progress/progress_edit_done.html', {'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = ProgressForm(instance=progress_record)
        else:
            form = GuestProgressForm(instance=progress_record)
        return render(request, 'karate/Progress/progress_edit.html', {'form': form, 'progress_record': progress_record, 'start_time': session_time})


def payment_edit(request, payment_id):
    session_time = request.session.get('user_session', None)
    if request.user.is_authenticated:
        payment_record = Payment.objects.get(id=payment_id)
    else:
        payment_record = GuestPayment.objects.get(id=payment_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PaymentForm(request.POST, instance=payment_record)
        else:
            form = GuestPaymentForm(request.POST, instance=payment_record)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'karate/Payment/payment_edit_done.html', {'form': form, 'start_time': session_time})
    else:
        if request.user.is_authenticated:
            form = PaymentForm(instance=payment_record)
        else:
            form = GuestPaymentForm(instance=payment_record)
        return render(request, 'karate/Payment/payment_edit.html', {'form': form, 'payment_record': payment_record, 'start_time': session_time})


def student_delete(request, student_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            student = Student.objects.get(id=student_id)
        else:
            student = GuestStudent.objects.get(id=student_id)
        name = student.first_name
        student.delete()
        return render(request, 'karate/Student/student_delete_done.html', {'name': name, 'start_time': session_time})
    else:
        return render(request, 'karate/Student/student_delete.html', {'student_id': student_id, 'start_time': session_time})


def parent_delete(request, parent_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            parent = Parent.objects.get(id=parent_id)
        else:
            parent = GuestParent.objects.get(id=parent_id)
        name = parent.first_name
        parent.delete()
        return render(request, 'karate/Parent/parent_delete_done.html', {'name': name, 'start_time': session_time})
    else:
        return render(request, 'karate/Parent/parent_delete.html', {'parent_id': parent_id, 'start_time': session_time})


def class_delete(request, class_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            class_record = Class.objects.get(id=class_id)
        else:
            class_record = GuestClass.objects.get(id=class_id)
        name = class_record.class_id
        class_record.delete()
        return render(request, 'karate/Class/class_delete_done.html', {'name': name, 'start_time': session_time})
    else:
        return render(request, 'karate/Class/class_delete.html', {'class_id': class_id, 'start_time': session_time})


def attendance_delete(request, attendance_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            attendance_record = Attendance.objects.get(id=attendance_id)
        else:
            attendance_record = GuestAttendance.objects.get(id=attendance_id)
        id = attendance_record.classroom.class_id
        date_taken = attendance_record.date_taken
        attendance_record.delete()
        return render(request, 'karate/Attendance/attendance_delete_done.html', {'date': date_taken, 'id': id, 'start_time': session_time})
    else:
        return render(request, 'karate/Attendance/attendance_delete.html', {'attendance_id': attendance_id, 'start_time': session_time})


def progress_delete(request, progress_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            progress_record = Progress.objects.get(id=progress_id)
        else:
            progress_record = GuestProgress.objects.get(id=progress_id)
        name = progress_record.student.first_name
        rank = progress_record.rank
        progress_record.delete()
        return render(request, 'karate/Progress/progress_delete_done.html', {'name': name, 'rank': rank, 'start_time': session_time})
    else:
        return render(request, 'karate/Progress/progress_delete.html', {'progress_id': progress_id, 'start_time': session_time})


def payment_delete(request, payment_id):
    session_time = request.session.get('user_session', None)
    if request.method == 'POST':
        if request.user.is_authenticated:
            payment_record = Payment.objects.get(id=payment_id)
        else:
            payment_record = GuestPayment.objects.get(id=payment_id)
        name = payment_record.student.first_name
        fee_type = payment_record.fee_type
        paid_date = payment_record.payment_date
        payment_record.delete()
        return render(request, 'karate/Payment/payment_delete_done.html', {'name': name, 'fee_type': fee_type, 'paid_date': paid_date, 'start_time': session_time})
    else:
        return render(request, 'karate/Payment/payment_delete.html', {'payment_id': payment_id, 'start_time': session_time})