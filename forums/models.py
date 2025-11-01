from django.db import models
from django.conf import settings
from courses.models import Course

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer to "{self.question.title}" by {self.user.username}'

    # ADD THESE TWO PROPERTIES to count votes
    @property
    def upvotes(self):
        return self.votes.filter(vote_type='up').count()

    @property
    def downvotes(self):
        return self.votes.filter(vote_type='down').count()

# ADD THIS NEW MODEL for voting
class Vote(models.Model):
    VOTE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)

    class Meta:
        # A user can only vote once per answer
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'{self.user.username} {self.vote_type}s {self.answer.id}'