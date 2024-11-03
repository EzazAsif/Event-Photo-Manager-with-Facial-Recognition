from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, PicsRelation
from django.db import transaction
from django.contrib import messages
import threading
import os
from django.conf import settings
from django.http import JsonResponse
import random
from FacialRecognition import testIndividual

User = get_user_model()  # Correctly get the User model

@login_required
def index(request):
    users = User.objects.all()  # Removed the instantiation
    return render(request, 'index.html', {'users': users})

@login_required
def myEvents(request):
    if request.user.is_authenticated:
        users = User.objects.all()  # Removed the instantiation
        events = Event.objects.filter(host=request.user)
        arrPics = []
        for event in events:
            try:
                arrPics.append(PicsRelation.objects.filter(event=event)[0])
            except:
                pass
        return render(request, 'events.html', {'events': events, 'users': users, 'pics':arrPics})
    else:
        return redirect("/")



def addEvents(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                name = request.POST.get('eventName')
                description = request.POST.get('eventDescription')
                event_date = request.POST.get('date')
                host = request.user

                # Create the Event instance
                code = str(random.randint(100000, 999999))
                event = Event.objects.create(name=name, description=description, event_date=event_date, host=host, code=code)
                

                # Handle the uploaded pictures
                eventPics = request.FILES.getlist('files[]')  # Change the key to 'files[]' to match Dropzone

                # Save multiple event pictures in the PicsRelation model
                for file in eventPics:
                    PicsRelation.objects.create(event=event, image=file)

            return redirect("/myEvents")

        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging purposes
            messages.error(request, "There was an error while creating the event. Please try again.")

            # Redirect to the same page to allow the user to fix the error
            return redirect("/")

    # If it's not a POST request, redirect to the home page
    return redirect("/")

def checkSimilarImages(user, event):
    event_ = Event.objects.get(id=event)
    pics = PicsRelation.objects.filter(event=event_)
    profilePic = user.profilepicture
    picsArr = []
    
    for pic in pics:
        image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
        picsArr.append(image_path)
    testIndividual([profilePic], picsArr)

def triggerRecognition(request, event):
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, event))
    thread.start()
    return redirect("/myEvents")

def addPhotos(request, eventID):
    if request.method == "POST":
        event = Event.objects.get(id=eventID)
        eventPics = request.FILES.getlist('file')  # Change the key to 'file' to match Dropzone
       # Save multiple event pictures in the PicsRelation model
        for file in eventPics:
            PicsRelation.objects.create(event=event, image=file)
            print(f"Picture saved for event: {event.name}")
    

    return redirect("/myEvents/"+eventID)


def eventPage(request, eventID):
    event = Event.objects.get(id=eventID)
    pictures = PicsRelation.objects.filter(event=event)
    return render(request, 'eventPage.html',{'event':event, 'photos':pictures})


