from django.shortcuts import render

from chat_app.models import Conversation


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Conversation.objects.all(),
    })


def room_view(request, room_id):
    # chat_room = Conversation.objects.get(name=room_id)
    return render(request, 'room.html', {
        # 'conversation': chat_room,
        # "user_id":user_id
    })