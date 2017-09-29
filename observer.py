from collections import defaultdict


class Observable():

    def __init__(self):
        self.events = defaultdict(list)

    def on(self, event, *handlers):
        def _on_wrapper(*handlers):
            self.events[event].extend(handlers)
            return handlers[0]
        if handlers:
            return _on_wrapper(*handlers)
        return _on_wrapper

    def off(self, event=None, *handlers):
        if not event:
            self.events.clear()
            return True
        if not event in self.events:
            raise ValueError('event not found')
        if not handlers:
            self.events.pop(event)
            return True
        for callback in handlers:
            if not callback in self.events[event]:
                raise ValueError('handler not found')
            while callback in self.events[event]:
                self.events[event].remove(callback)
        return True

    def once(self, event, *handlers):
        def _once_wrapper(*handlers):
            def _wrapper(*args, **kw):
                for handler in handlers:
                    handler(*args, **kw)
                self.off(event, _wrapper)
            return _wrapper
        if handlers:
            return self.on(event, _once_wrapper(*handlers))
        return lambda x: self.on(event, _once_wrapper(x))

    def trigger(self, event, *args, **kw):
        functions = self.events.get(event)
        if not functions:
            return False
        for event in functions:
            event(self, *args, **kw)
        return True


class Entity():

    event = Observable()

    def __init__(self):
        pass

    @event.on('message')
    def receive_message(self, message):
        print('@event.on(\'message\')', message)

    @event.once('killed')
    def die(self):
        print('@event.once(\'killed\')', 'I die just once!')


a = Entity()

a.event.trigger('message', 'hallo welt')
a.event.trigger('message', 'hallo welt')
a.event.trigger('message', 'hallo welt')

a.event.trigger('killed')
a.event.trigger('killed')
a.event.trigger('killed')