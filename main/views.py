from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm

# rooms = [
#     {"id":1, "name": "Introduction to frontend"},
#     {"id":2, "name": "Learn more django framework"},
#     {"id":3, "name": "Python discord server"}
# ]


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user )
            return redirect("home")
        
        else:
            messages.error(request,"Username or Password is incorrect!")


    return render(request, "main/login-signup.html",{"page_name": "login"})


def logout_page(request):
    logout(request)
    return redirect('home')


def sign_up(request):
    create_user_form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
            
        else:
            messages.error(request, "Error occured while signing in!")

    return render(request, "main/login-signup.html", {"create_user_form":  create_user_form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q) )

    recent_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

    room_counts = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics, "room_counts": room_counts, "recent_messages": recent_messages}
    return render(request, "main/home.html", context)
   

def user_profile(request, pk):
    user  = User.objects.get(id = pk)
    topics = Topic.objects.all()
    recent_messages = user.message_set.all()
    rooms = user.room_set.all()
    context= {"user":user, "topics":topics, "rooms": rooms, "recent_messages": recent_messages}
    return render(request, 'main/profile.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        Message.objects.create(
            user = request.user,
            room=room,
            body= request.POST.get("message")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)
        
    context = {"room": room, "room_messages": room_messages, "participants": participants}

    return render(request, "main/room.html", context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Request not allowed!")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')

    context = {
        "data": message
    }

    return render(request, "main/delete.html", context)
    # message = Message.object


@login_required(login_url='login')
def create_room(request):
    room_form = RoomForm()

    if request.method == "POST":
        room_form = RoomForm(request.POST)
        print(room_form)
        if room_form.is_valid():
            room = room_form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {"room_form": room_form}
    return render(request, "main/form.html", context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    room_form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("User not allowed!")

    if request.method == "POST":
        room_form = RoomForm(request.POST,instance=room)

        if room_form.is_valid():
            room_form.save()
            return redirect('home')

    context = {"room_form": room_form}

    return render(request, 'main/form.html', context)


@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("User not allowed")

    if (request.method == "POST"):
        room.delete()
        return redirect("home")
    
    return render(request, "main/delete.html", {"data": room})
        
