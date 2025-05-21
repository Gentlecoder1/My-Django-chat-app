from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ChatRoom, Message  # Import the correct model
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.views.decorators.http import require_GET

# Create your views here. 
def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'index.html', {'rooms': rooms})

def chatroom(request, room_name):
    username = request.GET.get('username')
    try:
        chatroom_details = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        return render(request, 'chatroom.html', {
            'username': username,
            'room_name': room_name,
            'chatroom_details': None,
            'error': f'Room "{room_name}" does not exist.'
        })
    return render(request, 'chatroom.html', {
        'username': username,
        'room_name': room_name,
        'chatroom_details': chatroom_details
    })

def checkview(request):
    room_name = request.POST.get('room_name')
    username = request.POST.get('username')

    if not room_name or not username:
        return redirect('index')

    room, created = ChatRoom.objects.get_or_create(name=room_name)

    # Correct use of reverse
    chatroom_url = reverse('chatroom', kwargs={'room_name': room_name})

    # ✅ Pass username and created as query parameters
    return redirect(f'{chatroom_url}?username={username}&created={created}')

def send(request):
    if request.method == "POST":
        username = request.POST.get('username')
        room_id = request.POST.get('room_id')
        message = request.POST.get('message')

        print("Received username:", username)
        print("Received room_id:", room_id)
        print("Received message:", message)

        if not username or not room_id or not message:
            print("Missing data!")
            return HttpResponse("Missing data", status=400)

        # Save the message with room as a string (room_id)
        msg = Message.objects.create(content=message, user=username, room=room_id)
        print("Message saved!")
        return HttpResponse("Message sent!")
    else:
        print("Invalid request method!")
        return HttpResponse("Invalid request", status=400)


def getmsg(request):
    if request.method == "GET":
        room_id = request.GET.get('room_id')
        messages = Message.objects.filter(room=room_id).order_by('date')
        messages_list = []
        for msg in messages:
            messages_list.append({
                'username': msg.user,  # user is a string
                'message': msg.content,
                'timestamp': msg.date.strftime("%H:%M")
            })
        return JsonResponse({'messages': messages_list})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@require_GET
def fetch_messages(request, room_name):
    print(f"Fetching messages for room: {room_name}")  # Debug print
    messages = Message.objects.filter(room=room_name).order_by('date')
    print(f"Found {messages.count()} messages in DB for this room.")  # Debug print
    data = [
        {
            'username': msg.user,
            'message': msg.content,
            'timestamp': msg.date.strftime('%I:%M %p')
        }
        for msg in messages
    ]
    print(f"Returning messages: {data}")  # Debug print
    return JsonResponse({'messages': data})