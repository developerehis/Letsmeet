from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone

# inbox functions
def inbox(request,profile_friend=None):
    profile = request.user.profile
    friends = profile.friends.all()

    if profile_friend is not None:
        p2 = friends.filter(id=profile_friend).first()
        new_chat = Chat()
        new_chat.save()
        m1 = Chat_members(chat=new_chat,profile=profile,deleted=False,last_viewed=timezone.now())
        m2 = Chat_members(chat=new_chat,profile=p2,deleted=False,last_viewed=timezone.now())
        m1.save()
        m2.save()
        return redirect('conversations:inbox')

    chat_ids = profile.chats.all().values_list('chat_id', flat=True)
    chats = Chat.objects.filter(id__in=chat_ids)
    chatting_with = []

    for c in chats:
        profile_chat_member = c.members.get(profile=profile)
        if profile_chat_member.deleted == False:
            friend_chat_member = c.members.exclude(profile=profile).first()
            chatting_with.append(friend_chat_member)
            friends = friends.exclude(user=friend_chat_member.profile.user)

    context = {
        'profile' :profile,
        'friends' :friends,
        'chat_details' : chatting_with,
    }
    return render(request, 'conversations/inbox.html', context)
