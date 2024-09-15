import graphene

from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Count

from functools import wraps

from graphql_jwt.decorators import login_required
from graphql import GraphQLError


from graphql_core.schema_types import (
    AccountType,
    BookType,
    BookRequestType,
)


from graphql_core.utils.base_mutation import BaseMutation
from graphql_core.utils.custom_jwt import CustomObtainJSONWebToken

from books.models import Books, BookRequest


User = get_user_model()




def get_today_date():
    return date.today()


def admin_or_staff_required(func):
    """checks if a user is an admin or staff"""
    @wraps(func)
    @login_required
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
      
        if not (user.is_staff or user.is_admin):
            raise GraphQLError("You have to be an admin or staff to perform this operation")
    
        return func(root, info, *args, **kwargs)
    
    return wrapper


class CreateAccountMutation(BaseMutation):
    account = graphene.Field(AccountType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=False)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        username = graphene.String(required=True)
        
    
    
    @classmethod
    def mutate(cls, root, info, **kwargs):

        user = User.objects.filter(email=kwargs['email']).first()
        
        if not user:
            user = User.objects.create(**kwargs)
            user.set_password(kwargs["password"])
            user.save(update_fields=["password"])
            return cls(success=True, message="Account created successfully.")
        
        else:
            return cls(success=False, errors={
                "email": f"{kwargs['email']}email exists"
            })


class SignInMutation(CustomObtainJSONWebToken):

    @classmethod
    def mutate(cls, root, info, **login_credentials):
        user = User.objects.filter(email=login_credentials['email']).first()

        if not user:
           return cls(success=False, errors={"error": "User not found"})
        
        if user and not user.check_password(login_credentials['password']):
           return cls(success=False, errors={'error':"invalid credentials"})
        
        if user and user.check_password(login_credentials["password"]):

            return super().mutate(root, info, **login_credentials)


class AddNewBookMutation(BaseMutation):
    book = graphene.Field(BookType)
    
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        genre = graphene.String(required=True)
        number_of_copies = graphene.Int(required=True)
        isbn = graphene.String(required=True)


    

    @admin_or_staff_required
    def mutate(root, info, **book_information):
    
        book_isbn = Books.objects.filter(isbn=book_information["isbn"]).first()

        if not book_isbn: 
            book = Books.objects.create(**book_information)
            return AddNewBookMutation(success=True, errors=None, message="Book information added successfully")

        else:
            return AddNewBookMutation(success=False, errors={"isbn": f"book with {book_information['isbn']} exists"})
        
    
    
class DeleteBookMutation(BaseMutation):
    book = graphene.Field(BookType)
    
    class Arguments:
        id = graphene.ID()

    

    @admin_or_staff_required
    def mutate(root, info, id):
        
        book = Books.objects.get(id=id)
        book.delete()

        return DeleteBookMutation(success=True, message="Book information deleted")
    

class BookRequestMutation(BaseMutation):
    
    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **book_request):
        user = info.context.user
        book = Books.objects.get(id=book_request['id'])
        BookRequest.objects.create(book=book, library_user=user)

        return cls(success=True, message="Book request made")

  
class CancelBookRequestMutation(BaseMutation):
    
    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **book_request):

        user = info.context.user
        book = BookRequest.objects.get(id=book_request['id'], library_user=user)
        
        book.book_request_status = BookRequest.CANCEL
        book.save(update_fields=['book_request_status'])
        return cls(success=True, message="Book request cancelled")
        



class Mutation(graphene.ObjectType):

    createAccount = CreateAccountMutation.Field()
    signIn = SignInMutation.Field()
    
    addNewBook = AddNewBookMutation.Field()
    deleteBook = DeleteBookMutation.Field()
    bookRequest = BookRequestMutation.Field()
    cancelBookRequest = CancelBookRequestMutation.Field()



class Query(graphene.ObjectType):
    
    book_count_in_the_library = graphene.String()
    book_requests_today = graphene.List(BookRequestType)
    book_with_most_requests_today =  graphene.List(BookType)

    @admin_or_staff_required
    def resolve_book_count_in_the_library(root, info):
        return Books.objects.count()

    @admin_or_staff_required
    def resolve_book_requests_today(root, info):
        return BookRequest.objects.filter(created_time__date=get_today_date()).order_by('-created_time')
    
    @admin_or_staff_required
    def resolve_book_with_most_requests_today(root, info):
        books_requested_today = BookRequest.objects.filter(created_time__date=date.today()) \
            .values('book__title', 'book__id') \
            .annotate(count=Count('book__title')) \
            .order_by('-count')
        
        if books_requested_today: 
            max_number_of_requested_book_today = books_requested_today.first()['count']        
            most_book_requested_today_ids = []

            for book in books_requested_today:
                if book['count'] == max_number_of_requested_book_today:
                    most_book_requested_today_ids.append(book['book__id'])
            
            return Books.objects.filter(id__in=most_book_requested_today_ids)
        
        return None



schema = graphene.Schema(mutation=Mutation, query=Query)
