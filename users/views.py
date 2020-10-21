from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


User = get_user_model()


@api_view(['POST'])
def obtain_auth_token(request):
    user = User.objects.filter(email=request.data.get('email')).first()

    if not user:
        content = {'detail': 'No active account found with the given credentials'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)})






def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
