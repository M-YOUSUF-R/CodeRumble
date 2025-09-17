from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question
from .serialize import QuestionSearlizer

# Create your views here.
@api_view(['GET'])
def getQuestions(request):
    category = request.GET.get('category')
    if category:
        questions = Question.objects.filter(category=category)
    else:
        questions = Question.objects.all()
    seralizer = QuestionSearlizer(questions,many=True)
    return Response(seralizer.data)
