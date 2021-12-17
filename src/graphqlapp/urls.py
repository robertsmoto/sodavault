from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import api_view, permission_classes


def graphql_token_view():
    view = GraphQLView.as_view(graphiql=True)
    view = permission_classes((IsAuthenticated,))(view)
    view = authentication_classes((TokenAuthentication,))(view)
    view = api_view(['GET', 'POST'])(view)
    return view


urlpatterns = [
    path('', graphql_token_view()),
    path(
        'graphql_notokenrequired',
        csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
