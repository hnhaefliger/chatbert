from source.whatsapp import whatsapp
import random

user = whatsapp.User()

while not(user.start()):
    input('scan the code to log in and press enter')

user.openChat('xxx')
messages = ['xxx']

while True:
    msgs, msgs_data = user.getMessages()

    if msgs_data[-1][1] != 'xxx':
        user.sendMessage(messages[random.randint(0, len(messages)-1)])
