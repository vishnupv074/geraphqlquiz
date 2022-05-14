from dataclasses import fields
from pyexpat import model
import graphene
from graphene_django import DjangoListField, DjangoObjectType
from .models import Question, Quizzes, Answer, Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")

class Query(graphene.ObjectType):
    all_quizzes = DjangoListField(QuizzesType)
    any_quizzes = graphene.Field(QuizzesType, id=graphene.Int())

    def resolve_any_quizzes(root, info, id):
        return Quizzes.objects.get(pk=id)

schema = graphene.Schema(query=Query)
