from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import QuizSession, QuizQuestion
from .ai_service import generate_question
from .adaptive_logic import update_level


@api_view(['POST'])
def start_quiz(request):
    session = QuizSession.objects.create()

    return Response({
        "session_id": session.id,
        "level": session.current_level
    })


@api_view(['GET'])
def get_question(request, session_id):

    session = QuizSession.objects.get(id=session_id)

    data = generate_question(session.current_level)

    if not data:
        return Response({"error": "AI generation failed"})

    question = QuizQuestion.objects.create(
        session=session,
        question=data["question"],
        option_a=data["options"]["A"],
        option_b=data["options"]["B"],
        option_c=data["options"]["C"],
        option_d=data["options"]["D"],
        correct_answer=data["correct_answer"],
        explanation=data["explanation"],
        level=session.current_level
    )

    return Response({
        "question_id": question.id,
        "level": question.level,
        "question": question.question,
        "options": {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c,
            "D": question.option_d,
        }
    })


@api_view(['POST'])
def submit_answer(request):

    question_id = request.data.get("question_id")
    user_answer = request.data.get("answer")

    question = QuizQuestion.objects.get(id=question_id)
    session = question.session

    correct = user_answer == question.correct_answer

    if correct:
        session.correct_answers += 1
    else:
        session.wrong_answers += 1

    session.current_level = update_level(session.current_level, correct)

    if session.correct_answers + session.wrong_answers >= 10:
        session.final_level = session.current_level

    session.save()

    return Response({
        "correct": correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "next_level": session.current_level
    })


@api_view(['GET'])
def quiz_result(request, session_id):

    session = QuizSession.objects.get(id=session_id)

    return Response({
        "correct": session.correct_answers,
        "wrong": session.wrong_answers,
        "final_level": session.final_level
    })