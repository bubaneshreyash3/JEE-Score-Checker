import os
try:
    from bs4 import BeautifulSoup
except:
    print('Please Install. BeautifulSoup4 Module')
    input()
    exit()

def checkPresent():
    if 'nt' in os.name and os.path.exists('Data\\Response.html') and os.path.exists('Data\\AnswerKey.html'):
        print('Found Response and AnswerKey.')
    elif 'posix' in os.name and os.path.exists('Data/Response.html') and os.path.exists('Data/AnswerKey.html'):
        print('Found Response and AnswerKey.')
    else:
        print("[ERROR] Response and/or AnswerKey Not Found!!")
        input()
        exit(-1)

class Question:
    def __init__(self, queid, ans):
        self.id = queid
        self.ans = ans

    def check(self, res:str):
        self.res = str(res)

        if len(self.ans) == 11:
            if '-' in self.res:
                return None
            elif self.res == self.ans:
                return '4'
            else:
                # print('here')
                return '-1'
        else:
            if '-' in self.res:
                return None
            elif self.res == self.ans:
                return '4'
            else:
                return '0'

class Result:
    def __init__(self, subject=None):
        self.subject = subject

        self.ques = {}

        self.correct_mcq = 0
        self.correct_num = 0
        self.incorrect_mcq = 0
        self.incorrect_num = 0
        self.unsolved = 0

        self.mks = 0
        self.totalMks = 100

    def addQue(self, queid, ans):
        self.ques[queid] = Question(queid, ans)

    
    def check(self,queid, res:str):
        a = self.ques[str(queid)].check(res) # couldn't think of better name :(
        res = str(res)
        if a != None:
            self.mks += int(a)
            # print(int(a))
            if a=='4':
                if len(res) == 11:
                    self.correct_mcq += 1
                else:
                    #print(len(res))
                    self.correct_num += 1
            else:
                if len(res) == 11:
                    self.incorrect_mcq += 1
                else:
                    self.incorrect_num += 1
        elif a == None:
                self.unsolved += 1

    def show(self):
        if self.subject:
            print(f'Subject: {self.subject}')
        else:
            print('Total:')

        print(f'Correct(MCQ, Num): {self.correct_mcq}, {self.correct_num} = {self.correct_mcq + self.correct_num}')
        print(f'Incorrect(MCQ, Num): {self.incorrect_mcq}, {self.incorrect_num} = {self.incorrect_mcq + self.incorrect_num}')
        print(f'Unsolved: {self.unsolved}')
        print(f'Score: {self.mks}\\{self.totalMks}')

    def __add__(*args):
        ret = Result()
        ret.totalMks = 0

        for i in ['incorrect_mcq', 'incorrect_num', 'correct_mcq', 'correct_num', 'unsolved', 'mks', 'totalMks']:
            for arg in args:
                cmd = f'ret.{i} += arg.{i}'
                exec(cmd)

        
        return ret


def checkResponse():
    global phy_result, chem_result, math_result

    if 'nt' in os.name:
        dir = 'Data\\'
    elif 'posix' in os.name:
        dir = 'Data/'

    with open(dir+'Response.html') as response:
        page = response.readlines()

    soup = BeautifulSoup(''.join(page), 'html.parser')

    section_list = soup.findAll('div', {'class': 'section-cntnr'})

    responses = {}

    for i in range(6):
        section = section_list[i]
        question_list = section.findAll('table', {'class': 'menu-tbl'})
        question_data = section.findAll('table', {'class': 'questionRowTbl'})

        for j in range(len(question_list)):
            question = question_list[j]
            tbl_data = question.findAll('tr')
            queid = str(tbl_data[1].findAll('td')[1].text)

            if i%2==0:
                myop = tbl_data[7].findAll('td')[1].text
                try:
                    opid = int(myop) + 1
                    myres = str(tbl_data[opid].findAll('td')[1].text)
                except ValueError:
                    myres = ' -- '
    

            else:
                question = question_data[j]
                myres = question.findAll('td')[5].text
                try:
                    float(myres)
                except ValueError:
                    myres = ' -- '

            if i==0 or i==1:
                phy_result.check(queid, myres)
            elif i==2 or i==3:
                chem_result.check(queid, myres)
            elif i==4 or i==5:
                math_result.check(queid, myres)


def getAnswers():
    global phy_result, chem_result, math_result

    if 'nt' in os.name:
        dir = 'Data\\'
    elif 'posix' in os.name:
        dir = 'Data/'

    with open(dir+'AnswerKey.html') as response:
        page = response.readlines()

    soup = BeautifulSoup(''.join(page), 'html.parser')

    answers = {
        'Physics' : {},
        'Chemistry' : {},
        'Maths' : {}
    }

    answer_tbl = soup.findAll('table')[1]
    que_str = 'ctl00_LoginContent_grAnswerKey_ctl{:02d}_lbl_QuestionNo'
    ans_str = 'ctl00_LoginContent_grAnswerKey_ctl{:02d}_lbl_RAnswer'

    count = 0

    for i in range(2, 92):
        que = que_str.format(i)
        ans = ans_str.format(i)

        queid = str(soup.find('span', {'id' : que}).text)
        answer = str(soup.find('span', {'id': ans}).text)

        if (i-2)<30:
            # sub = 'Physics'
            phy_result.addQue(queid, answer)
        elif (i-2)>29 and (i-2)<60:
            # sub = 'Chemistry'
            chem_result.addQue(queid, answer)
        else:
            # sub = 'Maths'
            math_result.addQue(queid, answer)

def main():
    checkPresent()
    
    '''phy_result = Result('Physics')
    chem_result = Result('Chemistry')
    math_result = Result('Maths')'''

    getAnswers()
    checkResponse()

    #phy_result.show()
    #print(phy_result.ques)
   

if __name__=='__main__':
    phy_result = Result('Physics')
    chem_result = Result('Chemistry')
    math_result = Result('Maths')
    
    checkPresent()
    print()

    getAnswers()
    checkResponse()
    total = phy_result + chem_result + math_result

    phy_result.show()
    print()
    chem_result.show()
    print()
    math_result.show()
    print()
    total.show()

    input()