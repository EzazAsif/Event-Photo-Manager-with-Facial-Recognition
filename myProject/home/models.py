from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_events') 
    guest = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='guest_events')
    event_date = models.DateField()
    published = models.BooleanField(default=False)
    code = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Event {self.name} hosted by {self.host.username}"


# PicsRelation model to relate a picture to a user (ForeignKey to Picture and User)
class PicsRelation(models.Model):
    event = models.ForeignKey(Event, related_name='pictures', default="", on_delete=models.CASCADE)  # Link multiple images to one event
    image = models.ImageField(upload_to='images/eventPictures', default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.name}"
    



class userPicsRelation(models.Model):
    image = models.ForeignKey(PicsRelation, on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='guest_pics')

    def __str__(self):
        return f"Image for {self.user}"
    
class AnonymousUserPicsRelation(models.Model):
    image = models.ForeignKey(PicsRelation, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.user}"