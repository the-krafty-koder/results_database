from django.shortcuts import render,redirect,HttpResponse
from .tables import *
from .form import *
from .models import *
from processing.functions import add_to_database,get_csv_data
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Create your views here.

def getStream(institution_name,form_name,stream_name):
    return Institution.objects.find(institution_name).get_class(form_name).get_stream(stream_name)

@login_required(login_url='/login')
def load_csv(request):
    if request.method == 'POST':
        form = upload_form(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            results = get_csv_data(request.FILES['file'].name,cd['file']).return_data()

            add_to_database(request.user.institution_name,cd["classes"]).add_exam_to_database(cd["streams"],
                    {"exam_name":cd["exam_name"],"year":cd["exam_year"],"term":cd["exam_term"],"cat":cd["exam_cat"]},results)
            return redirect('/load_base')

    else:
        form = upload_form()

    return render(request,"load_results_csv.html",{'form':form})

def load_list(request):
    classes = {form:[stream for stream in form.streams] for form in (clas for clas in Institution.objects.find(request.user.institution_name).classes)}
    return render(request,"load_list.html",{"classes":classes})

@login_required(login_url='/login')
def load_results(request):
    get_username(request.user.institution_name)
    if request.method == "POST":
        form = submit_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            add_to_database(request.user.institution_name,cd["classes"]).add_exam_to_database(cd["streams"],
                    {"exam_name":cd["exam_name"],"year":cd["exam_year"],"term":cd["exam_term"],"cat":cd["exam_cat"]},sucess())
            return redirect('/load_base')
    else:
        stream = getStream(request.user.institution_name,"Form 1","North")
        form = submit_form()

    return render(request,"load_results.html",{'form':form,"submission_table":get_tables().get_submit_app(stream)})

def load_base(request):
    return render(request,"base.html")

def load_load(request):
    return render(request,"loading_modal.html")

@login_required(login_url='/login')
def load_student(request):
    return render(request,"student_view.html",{'display_student':display_student_app})


def load_dashboard(request):
    subject_list = ()
    class_list = {}
    if request.method == "POST":
        subject_form = create_subject_form(request.POST)
        class_form = create_class_form(request.POST)
        edit_form = edit_class_form(request.POST)
        stream_form = add_stream_form(request.POST)

        if subject_form.is_valid():
            cd = subject_form.cleaned_data
            Subject.objects.create_subject(cd["name"],cd["type"],cd["group"],cd["code"])
            return redirect('load_dashboard')

        if class_form.is_valid():
            cd = class_form.cleaned_data
            add_to_database(request.user.institution_name,cd["name"]).add_class()
            return redirect('load_dashboard')

        if stream_form.is_valid():
            cd = stream_form.cleaned_data
            add_to_database(request.user.institution_name,cd["form_name"]).add_stream(cd["stream_name"],cd["class_teacher"])
            return redirect('load_dashboard')

        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            #add_to_database(request.user.institution_name,cd["form_name"]).add_stream(cd["stream_name"],cd["class_teacher"])
            return redirect('load_dashboard')
    else:
        subject_list = (subject for subject in Subject.objects.all())
        class_list = {clas:[len(clas.streams)] for clas in Institution.objects.find(request.user.institution_name).classes}
        subject_form = create_subject_form()
        class_form = create_class_form()
        edit_form = edit_class_form()
        stream_form = add_stream_form()
        institution = Institution.objects.find(request.user.institution_name)
    return render(request,"dashboard.html",{"subject_form":subject_form,"subject_list":subject_list,"class_form":class_form,"class_list":class_list,
        "edit_form":edit_form,"stream_form":stream_form,
        "institution":{"Institution":institution.institution_name,"Classes":len(institution.classes),"Subjects":len(list(Subject.objects.all())),"Total Students":300}})

@login_required(login_url='/login')
def load_stream(request,form_name,stream_name):

    stream = getStream(request.user.institution_name,form_name,stream_name)
    return render(request,"stream_view.html",{'lineplot1':get_tables().get_lineplot(),'streamview_table':get_tables().get_streamview_app(stream),"stream":stream,"class":form_name})

@login_required(login_url='/login')
def load_student_db(request):
    classes = {form:[stream for stream in form.streams] for form in (clas for clas in Institution.objects.find(request.user.institution_name).classes)}
    return render(request,"load_student_db.html",{"classes":classes})

@login_required(login_url='/login')
def view_student_db(request,form_name,stream_name,student_name=None):
    if request.method == "POST":
        form = new_student_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            add_to_database(request.user.institution_name,form_name).add_student_to_database(stream_name,{x:cd[x] for x in cd})
            return HttpResponse(cd.__str__())
    else:
        form = new_student_form()

    stream = getStream(request.user.institution_name,form_name,stream_name)
    return render(request,"display_student_db.html",{"student_db":get_tables().get_students_db(stream),"class":form_name,"form":form})

@login_required(login_url='/login')
def new_student(request):
    return render(request,"new_student.html")

@login_required(login_url='/login')
def edit_student(request,form_name,stream_name,student_name):
    if request.method == "POST":
        form = edit_student_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            add_to_database(request.user.institution_name,form_name).edit_student(stream_name,student_name,cd)
            return HttpResponse(cd.__str__())
    else:
        student = getStream(request.user.institution_name,form_name,stream_name).get_student(student_name)
        form = edit_student_form({"fname":student.fname,"lname":student.lname,"adm":student.admission,"contact":student.contact,"kcpe":student.kcpe,"email":student.email})

    return render(request,"edit_student.html",{"student":student,"form_name":form_name,"stream":stream_name,"form":form})

def edit_stream(request,form_name,stream_name):
    if request.method == "POST":
        form = add_stream_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            add_to_database(request.user.institution_name,form_name).edit_stream(stream_name,{"name":cd["stream_name"],"teacher":cd["class_teacher"]})
            return redirect('load_dashboard')
    else:
        stream = getStream(request.user.institution_name,form_name,stream_name)
        form = add_stream_form({"form_name":form_name,"stream_name":stream_name,"class_teacher":stream.class_teacher})

    return render(request,"edit_stream.html",{"stream_form":form})
