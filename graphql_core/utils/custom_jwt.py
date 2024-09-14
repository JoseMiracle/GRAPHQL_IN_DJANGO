import graphene
from graphene.types.generic import GenericScalar
from graphql_jwt import mixins
from graphql_jwt.settings import jwt_settings
from graphql_jwt.decorators import token_auth
from django.contrib.auth import get_user_model

from graphql_core.utils.base_mutation import BaseMutation

class CustomJSONWebTokenMixin:
    """Mixin to handle custom JWT fields"""

    payload = GenericScalar(required=True)
    refresh_expires_in = graphene.Int(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields["token"] = graphene.Field(graphene.String, required=False)
            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields["refresh_token"] = graphene.Field(
                    graphene.String, required=False
                )
        return super().Field(*args, **kwargs)


class CustomObtainJSONWebTokenMixin(CustomJSONWebTokenMixin):
    """Mixin to enforce resolve method in custom JWT mutation"""

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, "resolve", None), (
            f"{name or cls.__name__}.resolve method is required in a CustomJSONWebTokenMutation."
        )
        super().__init_subclass_with_meta__(name=name, **options)


class CustomJSONWebTokenMutation(CustomObtainJSONWebTokenMixin, BaseMutation):
    """Abstract class for handling JWT mutations"""

    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(required=True),
                "password": graphene.String(required=True),
            }
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(
            success=True,
            message="Token successfully obtained.",
            errors=None,  
            payload={"token": "your_token_value"},  
            refresh_expires_in=jwt_settings.JWT_EXPIRATION_DELTA.total_seconds()
        )
       


class CustomObtainJSONWebToken(CustomJSONWebTokenMutation, mixins.ResolveMixin):
    """Concrete JWT mutation to obtain token"""
    pass
