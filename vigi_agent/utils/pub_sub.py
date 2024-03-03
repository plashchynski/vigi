from queue import Queue
import threading

class PubSub:
    """
    A simple publish-subscribe (PubSub) class that allows multiple subscribers to
    receive messages from a single publisher on a single topic.
    """
    def __init__(self):
        self.subscribers = []
        # Lock to prevent race conditions when accessing the list of
        # subscribers from different threads
        self.lock = threading.Lock()

    def subscribe(self):
        """
        Subscribe to the PubSub object and return a queue to receive messages.
        """
        queue = Queue()
        with self.lock:
            self.subscribers.append(queue)
        return queue

    def unsubscribe(self, subscriber_queue):
        """
        Unsubscribe from the PubSub object.
        """
        with self.lock:
            self.subscribers.remove(subscriber_queue)

    def publish(self, message):
        """
        Publish a message to all the subscribers.
        """
        with self.lock:
            for subscriber in self.subscribers:
                subscriber.put(message, block = False)
