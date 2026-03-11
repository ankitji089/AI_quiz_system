from django.urls import path
from . import views

urlpatterns = [
    path('start-quiz/', views.start_quiz),
    path('question/<int:session_id>/', views.get_question),
    path('submit-answer/', views.submit_answer),
    path('result/<int:session_id>/', views.quiz_result),
]