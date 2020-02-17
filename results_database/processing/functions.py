import pandas as pd
from submission.models import *
from processing.models import *
from django.shortcuts import redirect


class add_to_database:

    def __init__(self,institution_name,class_name):
        self.institution = Institution.objects.find(institution_name)
        self.form = class_name

    def add_institution(self,name,address,website,logo,telephone):
        Institution.objects.create(name,address,website,logo,telephone)

    def add_class(self):
        self.institution.classes = self.institution.add_class(self.form)
        self.institution.save()

    def remove_class(self,class_name):
        self.institution.classes = self.institution.remove_class(class_name)
        self.institution.save()

    def add_stream(self,stream_name,class_teacher):
        self.institution.get_class(self.form).streams = self.institution.get_class(self.form).add_stream(stream_name,class_teacher)
        self.institution.save()

    def edit_stream(self,stream_name,stream):
        old_stream = self.institution.get_class(self.form).get_stream(stream_name)
        index = self.institution.get_class(self.form).streams.index(old_stream)
        old_stream.stream_name = stream["name"]
        old_stream.class_teacher = stream["teacher"]
        self.institution.get_class(self.form).streams[index] = old_stream
        self.institution.save()

    def remove_stream(self,stream_name):
        self.institution.get_class(self.form).streams = self.institution.get_class(self.form).remove_stream(stream_name)
        self.institution.save()

    def edit_student(self,stream_name,student_name,params):
        path = self.institution.get_class(self.form).get_stream(stream_name)
        student = path.get_student(student_name)
        index = path.students.index(student)
        student.fname = params["fname"]
        student.lname = params["lname"]
        student.adm = params["adm"]
        student.contact = params["contact"]
        student.email = params["email"]
        student.kcpe = params["kcpe"]
        student.student_name = "{} {}".format(params["fname"],params["lname"])
        self.institution.get_class(self.form).get_stream(stream_name).students[index] = student
        self.institution.save()

    def add_student_to_database(self,stream,student):

        if self.institution.check_class(self.form):

            if self.institution.get_class(self.form).check_stream(stream):
                # create new exam
                self.institution.get_class(self.form).get_stream(stream).students = self.institution.get_class(self.form).get_stream(stream).add_student(Student.objects.create_student(student["fname"],student["lname"],self.form,
                        student["adm"],student["contact"],student["email"],student["kcpe"]))
                self.institution.save()
            else:
                return "Stream not in database, add first to database"
        else:
            return "Class not in database, add first to database"

    def remove_student(self,stream,student_name):
        if self.institution.check_class(self.form):

            if self.institution.get_class(self.form).check_stream(stream):

                self.institution.get_class(self.form).get_stream(stream).students = self.institution.get_class(self.form).get_stream(stream).remove_student(student_name)
                self.institution.save()
            else:
                return "Stream not in database, add first to database"
        else:
            return "Class not in database, add first to database"


    def add_exam_to_database(self,stream,exam,result):

        if self.institution.check_class(self.form):

            if self.institution.get_class(self.form).check_stream(stream):
                # create new exam
                self.institution.get_class(self.form).get_stream(stream).exams = self.institution.get_class(self.form).get_stream(stream).add_exam(Exam.objects.create(exam_name = exam["exam_name"], year = exam["year"], term = exam["term"],cat = exam["cat"],results = result))
                self.institution.save()
            else:
                return "Stream not in database, add first to database"
        else:
            return "Class not in database, add first to database"

class get_csv_data():

    def __init__(self,filename,file):
        self.file = file
        self.filename = filename

    def validate(self,filename):
        return filename.endswith('.csv')

    def read(self,filename,file):
        while(self.validate(filename)):
            return pd.read_csv(file)

    def return_data(self):
        df = self.read(self.filename,self.file)
        columns = ["Admission","Name"]
        columns.extend(["Maths","English","Kiswahili"])
        return df[columns]

def get_data(model):
    data = {x.name: model._meta.get_fields()[model._meta.get_fields().index(x)].value_from_object(model) for x in model._meta.get_fields()}
    data["image"] = None
    return pd.Series(data)

def get_student_name(form_name,stream_name,student_name):
    return redirect('/edit_student/{}/{}')
