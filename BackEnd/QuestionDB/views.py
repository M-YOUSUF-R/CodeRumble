from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from .serialize import QuestionSearlizer

# Create your views here.
@api_view(['GET'])
def getQuestions(request):
    category = request.GET.get('category')
    if category:
        questions = Question.objects.filter(q_category=category)
        print(questions)
    else:
        questions = Question.objects.all()
    seralizer = QuestionSearlizer(questions,many=True)
    return Response(seralizer.data)

@api_view(['GET'])
def dataEntry(request):
    return render(request,'QuestionDB/index.html')

@api_view(['POST'])
def insertQuestion(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        question = request.POST.get('question')
        testcase = request.POST.get('testcase')
        answer = request.POST.get('answer')

        question = Question(q_category=category,q_title=title,question=question,q_testcase=testcase,q_answer=answer)
        question.save()

        return HttpResponse('data insert successfully')
    else:
        return HttpResponse('somethings went wrong: invalid request method')



