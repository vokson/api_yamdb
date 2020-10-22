from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from .models import MyUserManager
from .serializers import MyUserSerializer, UserSerializer
from .permissions import IsMyself, IsAdminRole
from rest_framework.reverse import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect

import uuid
from loguru import logger

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

        user.confirmation_code = uuid.uuid4()
        user.save()

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


class MyUserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsMyself]

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'me':
            return self.request.user

        return super(MyUserViewSet, self).get_object()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole | IsAdminUser]
    filterset_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        # permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        url = reverse_lazy('myuser-detail', args=[self.request.user.username], request=request)
        logger.debug(url)

        return HttpResponseRedirect(redirect_to=url)
        # return self.retrieve(request=request, pk=self.request.user.username)