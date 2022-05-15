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

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)
    
    all_category = DjangoListField(CategoryType)
    def resolve_all_category(root, info):
        return Category.objects.all()


class CategoryMutationAdd(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutationAdd(category=category)

class CategoryMutationUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutationUpdate(category=category)

class CategoryMutationDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return 


class Mutation(graphene.ObjectType):
    add_category = CategoryMutationAdd.Field()
    update_category = CategoryMutationUpdate.Field()
    delete_category = CategoryMutationDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
