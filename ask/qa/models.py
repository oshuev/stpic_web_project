from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name='question_author')
    likes = models.ManyToManyField(User, related_name='question_likes')

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse('question', 
            kwargs={'slug': self.id})
        
    class Meta:
        db_table = 'qa_question'


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User, related_name='answer_author')

    class Meta:
        db_table = 'qa_answer'