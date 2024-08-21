from django.db import models


class Message(models.Model):
  sender = models.CharField(max_length=150,)
  reciever = models.CharField(max_length=150,)
  message = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)


  def get_chat_list_usernames(username):
    sended = Message.objects.filter(sender=username).values_list("reciever", flat=True)
    recieved = Message.objects.filter(reciever=username).values_list("sender", flat=True)
    
    usernames = set(sended) | set(recieved)

    if username in usernames:
      usernames.remove(username)
    
    return usernames
  
  def get_messages_for_chat(user1, user2):
    messages = Message.objects.filter(sender=user1, reciever=user2) | \
      Message.objects.filter(sender=user2, reciever=user1)
    
    return messages.order_by("timestamp")

  def __str__(self):
    return f'{self.sender} - {self.reciever} - {self.message[:10]}'