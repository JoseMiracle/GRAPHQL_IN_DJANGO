import graphene

from accounts.models import User

from books.models import Books, BookRequest

from graphene_django import DjangoObjectType
from graphene_django.utils import camelize

class AccountType(DjangoObjectType):
    class Meta:
        model = User
    
class BookType(DjangoObjectType):
    class Meta:
        model = Books
    

class BookRequestType(DjangoObjectType):
    class Meta:
        model = BookRequest


class ErrorType(graphene.Scalar):
    
    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        raise Exception("`errors` should be dict!")