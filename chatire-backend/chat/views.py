from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import ChatSession, ChatSessionMember, ChatSessionMessage, deserialize_user


class ChatSessionView(APIView):
    """Create and manage chat sessions."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Create a new chat session."""
        user = request.user
        chat_session = ChatSession.objects.create(owner=user)
        ChatSessionMember.objects.create(chat_session=chat_session, user=user)

        return Response({
            'status': 'SUCCESS',
            'uri': chat_session.uri,
            'message': 'New chat session created'
        })

    def patch(self, request, *args, **kwargs):
        """Add a user to an existing chat session."""
        uri = kwargs.get('uri')
        username = request.data.get('username')

        if not uri or not username:
            return Response({'error': 'URI and username required'}, status=400)

        User = get_user_model()
        user = User.objects.get(username=username)
        chat_session = ChatSession.objects.get(uri=uri)

        # Add user if not already a member
        ChatSessionMember.objects.get_or_create(chat_session=chat_session, user=user)

        owner = deserialize_user(chat_session.owner)
        members = [deserialize_user(member.user) for member in chat_session.members.all()]
        members.insert(0, owner)  # make the owner the first member

        return Response({
            'status': 'SUCCESS',
            'members': members,
            'message': f'{user.username} joined the chat',
            'user': deserialize_user(user)
        })


class ChatSessionMessageView(APIView):
    """Handle chat messages (GET history, POST new messages)."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Return all messages in a chat session."""
        uri = kwargs.get('uri')
        chat_session = ChatSession.objects.get(uri=uri)
        messages = [m.to_json() for m in chat_session.messages.all().order_by('create_date')]
        return Response({
            'id': chat_session.id,
            'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """Create a new message in a chat session."""
        uri = kwargs.get('uri')
        message_text = request.data.get('message')
        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        if not message_text:
            return Response({'error': 'Message text is required'}, status=400)

        chat_message = ChatSessionMessage.objects.create(
            user=user,
            chat_session=chat_session,
            message=message_text
        )

        return Response({
            'status': 'SUCCESS',
            'uri': chat_session.uri,
            'message': message_text,
            'user': deserialize_user(user)
        })
