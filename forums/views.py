from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course
from .models import Question, Answer, Vote
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required

@login_required
def question_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(course=course).order_by('-created_at')
    context = {
        'course': course,
        'questions': questions,
    }
    return render(request, 'forums/question_list.html', context)

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.all().order_by('created_at')
    
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            # FIX: Removed 'forums:' namespace to match your urls.py
            return redirect('question_detail', question_id=question.id)
    else:
        answer_form = AnswerForm()
        
    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
    }
    return render(request, 'forums/question_detail.html', context)

@login_required
def add_question(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course
            question.user = request.user
            question.save()
            # FIX: Removed 'forums:' namespace to match your urls.py
            return redirect('question_list', course_id=course.id)
    else:
        form = QuestionForm()
    return render(request, 'forums/question_form.html', {'form': form, 'course': course})

@login_required
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['up', 'down']:
        return redirect('question_detail', question_id=answer.question.id)

    existing_vote = Vote.objects.filter(user=request.user, answer=answer).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(user=request.user, answer=answer, vote_type=vote_type)

    # FIX: Removed 'forums:' namespace to match your urls.py
    return redirect('question_detail', question_id=answer.question.id)