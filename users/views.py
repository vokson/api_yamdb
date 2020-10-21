from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import mixins, viewsets

from .models import MyUserManager
from .serializers import UserSerializer
from .permissions import IsMyself

User = get_user_model()




@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_confirmation_code(request):

    email = request.data.get('email')

    if not email:
        return Response(
            {'email': 'Users must have an email address'},
            status=status.HTTP_400_BAD_REQUEST
        )

    email = MyUserManager.normalize_email(email)
    user = User.objects.filter(email=email).first()

    if not user:
        try:
            validate_email(email)
        except ValidationError as e:
            return Response(
                {'email': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            email=email,
            password=''
        )

    confirmation_code = user.confirmation_code

    send_mail(
        'Api YamDb - Confirmation',
        f'Your confirmation code is {confirmation_code}',
        'api@yamdb.com',
        [email],
        fail_silently=False,
    )

    return Response({'email': email})


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    user = User.objects.filter(
        email=request.data.get('email'),
        confirmation_code=request.data.get('confirmation_code'),
    ).first()

    if not user:
        content = {'detail': 'No active account found with the given credentials'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)})


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself, ]

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'me':
            return self.request.user

        return super(UserViewSet, self).get_object()

    # def get_queryset(self):
        # return User.objects.filter(pk=self.request.user.pk)
