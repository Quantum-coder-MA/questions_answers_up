from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random
from django.urls import reverse
from .models import Category, Question

def home(request):
    context = {'categories': Category.objects.all()}
    
    if request.GET.get('category'):
        category = request.GET.get('category')
        url = reverse('questions_answers') + f'?category={category}'
        return redirect(url)
    
    return render(request, 'home.html', context)

def questions_answers(request):
       
        question_objs = Question.objects.all()
        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        
        question_objs = list(question_objs)
        random.shuffle(question_objs)
        
        data = []
        for question in question_objs:
            data.append({
                "category": question.category.category_name,
                "question_text": question.question_text,
                "marks": question.marks,
                "answer": question.get_Answer()
            })
        
        payload = {'data': data}

        return render(request, 'questions_answers.html', payload)


def get_questions_answers(request):
    try:
        question_objs = Question.objects.all()
        category_objs = Category.objects.all()
        
        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))

        data = {
            "categories": []
        }

        for category in category_objs:
            related_questions = question_objs.filter(category=category)
            question_list = []
            
            for question in related_questions:
                question_list.append({
                    "question_text": question.question_text,
                    "marks": question.marks,
                    "answer": question.get_Answer()  
                })
            
            data["categories"].append({
                "name": category.category_name,
                "questions": question_list
            })
        
        payload = {'status': True, 'data': data}
        return JsonResponse(payload)
    
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

def submit(request):
    if request.method == 'POST':
        user_answers = request.POST
        score = 0
        total_marks = 0
        correct_answers = {}

        
        for key, value in user_answers.items():
            if key == 'csrfmiddlewaretoken':  
                continue

            
            question = Question.objects.get(question_text=key)

            
            correct_answer = None
            for ans in question.get_Answer():
                if ans['is_correct']:  
                    correct_answer = ans['answer']
                    break

            correct_answers[question.question_text] = correct_answer  

            
            if value == correct_answer:
                score += question.marks  

            total_marks += question.marks  

        score_percentage = (score / total_marks) * 100 if total_marks > 0 else 0

        context = {
            'score': score,
            'total_marks': total_marks,
            'score_percentage': score_percentage,
            'correct_answers': correct_answers,
            'user_answers': user_answers,
        }



        return JsonResponse(context)
