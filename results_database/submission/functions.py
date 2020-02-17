from .models import Subject

class validate_result:

    def __init__(self,result_dataframe):
        self.results = result_dataframe
        self.subjects  = Subject.objects.all()
        self.erros = []

    def min_subject(self, result):
		if(!(result['basic'] == 3)):
			return False
		if(!(result['science'] >=  2)):
			return False
		if(!(result['humanities'] >= 1)):
			return False
		if(!(result['tech1'] >= 1) OR (result['tech2'] >= 1) OR (result['humanities'] >= 2) OR (result['science'] >= 3)):
			return False
		return True

    def group_result(self,student_result):

        while self.subjects.count() > 0:
            subjects = {sub:sub.code for sub in self.subjects}

            for key in student_result:
                checker = {'basic':0,'science':0,'humanities':0,'tech1':0,"tech2":0}
                for sub in subjects:
                    try:
                        if subject[student_result["key"][sub]] in range(100,200):
                            checker['basic'] += 1
                        elif subject[student_result["key"][sub]] in range(200,300):
                            checker['science'] += 1
                        elif subject[student_result["key"][sub]] in range(300,400):
                            checker['humanities'] += 1
                        elif subject[student_result["key"][sub]] in range(400,500):
                            checker['tech1'] += 1
                        else:
                            checker['tech2'] += 1
                    except IndexError:
                        return "{} not in student result".format(sub)
                return True if self.min_subject(checker)==True else "{}'s subject details does not meet minimum requirements ".format(student_result[key])

    def validate(self):
		#check if  subject are atleasest seven
        data = self.results.to_dict('rows')
        return True if self.groupResults(data) is True

    @static_method
    def harmoniseResult(self , result):
        result.fillna("x", inplace = True)
		return result
