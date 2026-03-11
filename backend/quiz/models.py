from django.db import models


class QuizSession(models.Model):
    current_level = models.IntegerField(default=1)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    final_level = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id}"


class QuizQuestion(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)

    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=1)

    explanation = models.TextField()

    level = models.IntegerField()

    def __str__(self):
        return self.question