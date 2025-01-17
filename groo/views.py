from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import mysql.connector as conn

db =conn.connect(user='sql6429261',passwd='Mf3Q6WaXqp',host='sql6.freemysqlhosting.net',db='sql6429261')
curr=db.cursor(buffered=True)

# Create your views here.
def index(request):
    return HttpResponse("Home Page abhi tk nhi bna h...")

def signup(request):
    return render(request,'index.html')

def formsignup(request):
    if request.method == 'POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = User.objects.create_user(name, email, password)
        user.save()
    
    return redirect('index')

def login(request):
    return render(request,'index.html')

def formlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return home(request)
        else:
            return redirect('signup')

    
    return HttpResponse('Kuch to gadbad h daya')


def question(request):
    return render(request,'addquestion.html')

def addquestion(request):
    if request.method == 'POST':
        question=request.POST.get('question')
        my_query='''INSERT INTO questions(question)
        VALUES(%s)'''
        val=(question,)
        curr.execute(my_query,val)
        db.commit()

    return home(request)
    
def home(request):
    curr.execute('''SELECT * FROM questions''')
    parameters={'ques':curr}
    return render(request,'home.html',parameters)

def showanswers(request):
    if request.method == 'POST':
        ques_no=request.POST.get('ques_no')
        my_query='''SELECT answer FROM answers WHERE ques_no=%s'''
        val=(ques_no,)
        curr.execute(my_query,val)
        parameter={'answers':curr}
        return render(request,'displayanswers.html',parameter)


def addans(request):
    return render(request,'addans.html')

def anssubmit(request):
    if request.method == 'POST':
        ques_no=request.POST.get('ques_no')
        answer=request.POST.get('answer')
        my_query='''INSERT INTO answers (ques_no,answer) VALUES (%s,%s)'''
        val=(ques_no,answer)
        curr.execute(my_query,val)
        db.commit()
        return home(request)