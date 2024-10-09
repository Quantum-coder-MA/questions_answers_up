from django.db import models

# Create your models here.
from django.db import models
import uuid
import random
# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)    
    class Meta:
        abstract = True



class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.category_name
    

    
class Question(BaseModel):
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)
    def __str__(self) -> str:
        
        
        return self.question_text
    
    
    
    def get_Answer(self):
        
        answer_objs = list(Answer.objects.filter(question = self))
        random.shuffle(answer_objs)
        data = []
        
        for answer_objs in answer_objs:
            
            data.append({
                
                "answer" : answer_objs.answer_text,
                
                "is_correct": answer_objs.is_correct,
              
            })
        return data
    
class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)