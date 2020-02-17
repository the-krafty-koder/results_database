from djongo import models
from picklefield.fields import PickledObjectField

# Create your models here.
class subject_manager(models.Manager):
    def create_subject(self,name,typeof,group,code):
        subject  = self.create(name=name,type=typeof,group=group,code=code)
        return subject

    def remove_subject(self,subject):
        self.subjects.pop(self.subjects.index(subject))

    def get_subjects(self):
        return self.subjects


class Subject(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    group = models.CharField(max_length=30)
    code = models.CharField(max_length=30)

    objects = subject_manager()


class ExamManager(models.Manager):
    def create_exam(self, year, term, cat, results):
        exam = self.create(year=year,term=term,cat=cat,results=results)
        return exam

class Exam(models.Model):
    exam_name = models.CharField(max_length=10,primary_key=True)
    year = models.CharField(max_length=4)
    term = models.IntegerField()
    cat  = models.IntegerField()
    results = PickledObjectField(default="Null", null=True)

    objects = ExamManager()

    def __str__(self):
        return self.exam_name

class StudentManager(models.Manager):
    def create_student(self, fname,lname,form,adm,contact,email,kcpe,image=None):
        student = self.create(fname=fname,lname=lname,form=form,admission=adm,contact=contact,email=email,kcpe=kcpe,image=image,student_name="{} {}".format(fname,lname))
        return student

class Student(models.Model):

    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    form = models.CharField(max_length=20)
    admission = models.IntegerField()
    contact = models.IntegerField()
    email = models.EmailField()
    kcpe = models.TextField(max_length=20)
    image = models.ImageField()

    student_name = models.CharField(max_length=50,primary_key=True)

    def __str__(self):
        return "{} {}".format(self.fname,self.lname)

    objects = StudentManager()



class StreamManager(models.Manager):
    def create_stream(self, name, teacher,students=[],exams=[]):
        stream = self.create(stream_name=name, class_teacher=teacher, students=students, exams=exams)
        # do something with the book
        return stream


class Stream(models.Model):
    stream_name = models.CharField(max_length=40,primary_key=True)
    class_teacher = models.CharField(max_length=30)
    students = models.ArrayModelField(
        model_container = Student,
        blank=True,
    )
    exams = models.ArrayModelField(
        model_container =  Exam,
        blank=True,
    )

    objects = StreamManager()

    def __str__(self):
        return self.stream_name

    def check_student(self,value):
        for x in self.students:
            if x.student_name==value:return True

    def add_student(self, student):
        if (self.check_student("{} {}".format(student.fname,student.lname)))==True:
            return 'Student already  exists'
        else:
            new_students = [obj for obj in self.students]
            new_students.append(student)

            return new_students


    def remove_student(self,value):
        for x in self.students:
            if x.student_name==value:
                new_students = self.students
                new_students.pop(new_students.index(x))
                return new_students

    def get_student(self, value):
        for x in self.students:
            if x.student_name==value:return x

    def check_exam(self,value):
    	for x in self.exams:
            if(x.exam_name==value):return True

    def add_exam(self,exam):
        if (self.check_exam(exam.exam_name))==True:
            return 'Exam already  exists'
        else:
            new_exams = [obj for obj in self.exams]
            new_exams.append(exam)

            return new_exams


    def remove_exam(self,value):
        for x in self.exams:
             if x.exam_name==value:self.exams.pop(self.exams.index(x))

    def get_exam(self, value):
        for x in self.exams:
            if x.exam_name==value:return x


class ClassManager(models.Manager):
    def create_class(self, name,streams=[]):
        clas = self.create(class_name=name,streams=streams)
        return clas

class Class(models.Model):
    class_name = models.CharField(max_length=20,primary_key=True)
    streams = models.ArrayModelField(
        model_container=Stream,
        blank=True,
    )

    objects = ClassManager()

    def __str__(self):
        return self.class_name

    def check_stream(self,value):
        for x in self.streams:
             if(x.stream_name==value):return True

    def add_stream(self, value,teacher):
        if (self.check_stream(value))==True:
            return 'Class already  exist'
        else:
            newstream = [obj for obj in self.streams]
            newstream.append(Stream.objects.create_stream(value,teacher))

            return newstream




    def remove_stream(self,value):
        for x in self.streams:
            if x.stream_name==value:
                new_streams = self.streams
                new_streams.pop(new_streams.index(x))
                return new_streams



    def get_stream(self, value):
        for x in self.streams:
            if x.stream_name==value:return x

class InstitutionManager(models.Manager):
    def create_institution(self, name,address,website,telephone,logo=None,classes=[]):
        Institution = self.create(institution_name=name,address=address,website=website,logo=logo,telephone=telephone,classes=classes)

        return Institution

    def find(self,institution_name):
        return self.filter(institution_name = institution_name)[0]



class Institution(models.Model):

    institution_name = models.CharField(max_length=20,primary_key=True)
    address = models.TextField(max_length=20)
    website = models.CharField(max_length=30)
    telephone = models.IntegerField()
    logo = models.ImageField()
    classes = models.ArrayModelField(
        model_container=Class,
        blank=True,
    )

    objects = InstitutionManager()

    def __str__(self):
        return "{} {}".format(self.institution_name,self.address)

    def check_class(self,value):
        for x in self.classes:
            if x.class_name==value:return True

    def add_class(self, value):
        if (self.check_class(value))==True:
            return "Class already exists"
        new_classes = [obj for obj in self.classes]
        new_classes.append(Class.objects.create_class(value))

        return new_classes

    def remove_class(self,value):
        for x in self.classes:
            if x.class_name==value:
                new_classes = self.classes
                new_classes.pop(new_classes.index(x))
                return new_classes

    def get_class(self, value):
        for x in self.classes:
            if x.class_name==value:return x
