from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id":1, "name": "Introduction to frontend"},
#     {"id":2, "name": "Learn more django framework"},
#     {"id":3, "name": "Python discord server"}
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q) )
    room_counts = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics, "room_counts": room_counts}
    return render(request, "main/home.html", context)
   


def room(request, pk):
    room = Room.objects.get(id=pk)
    # room = None
    # for single_room in rooms:
    #     if single_room['id'] == int(pk):
    #         room = single_room
    context = {"room": room}

    return render(request, "main/room.html", context)


def create_room(request):
    room_form = RoomForm()

    if request.method == "POST":
        room_form = RoomForm(request.POST)

        if room_form.is_valid():
            room_form.save()
            return redirect('home')

    context = {"room_form": room_form}
    return render(request, "main/form.html", context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    room_form = RoomForm(instance=room)

    if request.method == "POST":
        room_form = RoomForm(request.POST,instance=room)

        if room_form.is_valid():
            room_form.save()
            return redirect('home')

    context = {"room_form": room_form}

    return render(request, 'main/form.html', context)


def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if (request.method == "POST"):
        room.delete()
        return redirect("home")
    
    return render(request, "main/delete.html", {"room": room})
        
