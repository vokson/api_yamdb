import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MyUserManager
from .permissions import IsAdminRole
from .serializers import UserSerializer

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

    send_mail(
        'Api YamDb - Confirmation',
        f'Your confirmation code is {user.confirmation_code}',
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole | IsAdminUser]
    filterset_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
