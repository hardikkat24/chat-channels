from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q


class ThreadManager(models.Manager):
    def by_user(self, user):
        lookup1 = Q(first=user) | Q(second=user)
        lookup2 = Q(first=user) & Q(second=user)
        qset = self.get_queryset().filter(lookup1).exclude(lookup2).distinct()
        return qset

    def get_or_create(self, user, other_username):
        # user is object but other_username not user object
        username = user.username
        if username == other_username:
            return None
        lookup1 = Q(first__username=username) & Q(second__username=other_username)
        lookup2 = Q(first__username=other_username) & Q(second__username=username)
        qset = self.get_queryset().filter(lookup1 | lookup2).distinct()

        if qset.count() == 1:
            return qset.first(), False
        elif qset.count() > 1:
            return qset.order_by('timestamp').first(), False
        else:
            c = user.__class__
            user2 = c.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_thread_first")
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_thread_second")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f"chat_{self.id}"
    """
    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user = "admin")
            return True
        return False
    """




class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="sender", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)