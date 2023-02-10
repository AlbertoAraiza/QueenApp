from firebase_admin import messaging

message = "I'm a message"

def sendNotification(token, title, message):
    message = messaging.Message(token = token,
        notification=messaging.Notification(
        title=title,
        body= message,
    ))
    response = messaging.send(message)
    print(response)