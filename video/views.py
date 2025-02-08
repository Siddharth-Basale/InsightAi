from django.shortcuts import render

def room(request, room_name):
    """Render the video chat room."""
    return render(request, 'video/room.html', {
        'room_name': room_name
    })