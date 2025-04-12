class Event:
    def __init__(self):
        self._listeners = []

    def add_listener(self, listener, *args, **kwargs):
        # Store the listener and its arguments in the form of a lambda function
        self._listeners.append((listener, args, kwargs))

    def remove_listener(self, listener):
        # Remove listener from the list
        self._listeners = [(l, a, k) for l, a, k in self._listeners if l != listener]

    def invoke(self):
        # Invoke the listeners and let them handle their arguments
        for listener, args, kwargs in self._listeners:
            listener(*args, **kwargs)