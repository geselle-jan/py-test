from collections import deque


class Message():

    def __init__(self, sender, receiver, name, data, delay=0):
        self.sender = sender
        self.receiver = receiver
        self.name = name
        self.data = data
        self.delay = delay

    def __repr__(self):
        return 'Message( {}, {}, {}, {} )'.format(
            self.sender,
            self.receiver,
            self.name,
            self.data
        )


class MessageQueue():

    messages = deque()

    def __init__(self):
        pass

    def add(self, message):
        self.messages.append(message)

    def send(self, message):
        message.receiver.on_message(message)

    def dispatch(self):
        while len(self.messages) > 0:
            message = self.messages.popleft()
            self.send(message)


message_queue = MessageQueue()


class Entity():

    def __init__(self):
        pass

    def __repr__(self):
        return 'Entity()'

    def send_message(self, receiver, name, data):
        msg = Message(self, receiver, name, data)
        message_queue.send(msg)

    def add_message(self, receiver, name, data):
        msg = Message(self, receiver, name, data)
        message_queue.add(msg)

    def on_message(self, message):
        pass


class Unit(Entity):
    name = ''
    health = 100
    damage = 5
    xp = 0

    def __init__(self, name):
        super(Unit, self).__init__()
        self.name = name

    def __repr__(self):
        return 'Unit(\'{}\')'.format(self.name)

    def say(self, text):
        print(
            '{}: {}'.format(
                self.name,
                text
            )
        )

    def status(self, text):
        print(
            ' -- {} {}'.format(
                self.name,
                text
            )
        )

    def on_message(self, message):
        super(Unit, self).on_message(message)
        if message.name == 'damage':
            self.handle_damage(message)
        if message.name == 'xp':
            self.handle_xp(message)

    def handle_damage(self, message):
        self.health -= message.data
        msg = Message(self, message.sender, 'xp', 10)
        message_queue.add(msg)
        self.say('AUA!!!')
        self.status('lost {} health'.format(message.data))

    def handle_xp(self, message):
        self.xp += message.data
        self.status('earned {} xp'.format(message.data))

    def attack(self, entity):
        self.say('GRR!!!')
        msg = Message(self, entity, 'damage', self.damage)
        message_queue.send(msg)


a = Unit('Horst')
b = Unit('Peter')

print(' -- {} has {} health'.format(b.name, b.health))

print(' -- fight starts')

a.attack(b)
a.attack(b)
a.attack(b)
a.attack(b)
a.attack(b)
a.attack(b)
b.attack(b)

print(' -- {} has {} health'.format(b.name, b.health))

print(' -- fight ends')

print(' -- {} has {} xp'.format(a.name, a.xp))

print(' // message_queue gets dispatched')

message_queue.dispatch()

print(' -- {} has {} xp'.format(a.name, a.xp))
