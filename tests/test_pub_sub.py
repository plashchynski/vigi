"""
Tests for the PubSub class.
"""

import unittest
import queue

from vigi.utils.pub_sub import PubSub

class TestPubSub(unittest.TestCase):
    """
    Test the PubSub class
    """
    def test_single_subscription(self):
        """Test that a single subscriber receives messages."""

        pubsub = PubSub()
        q = pubsub.subscribe()

        test_message = "Hello, World!"
        pubsub.publish(test_message)

        self.assertEqual(q.get(), test_message)
        pubsub.unsubscribe(q)


    def test_multiple_subscriptions(self):
        """Test that multiple subscribers receive messages."""

        pubsub = PubSub()
        queues = [pubsub.subscribe() for _ in range(3)]
        test_message = "Hello, Multiworld!"
        pubsub.publish(test_message)

        for q in queues:
            self.assertEqual(q.get(), test_message)
            pubsub.unsubscribe(q)

    def test_unsubscribe(self):
        """Test that unsubscribing prevents receiving messages."""
        pubsub = PubSub()
        queue1 = pubsub.subscribe()
        queue2 = pubsub.subscribe()
        pubsub.unsubscribe(queue1)

        test_message = "Test Unsubscribe"
        pubsub.publish(test_message)

        # queue1 should not receive any messages since it's unsubscribed
        with self.assertRaises(queue.Empty):
            queue1.get(timeout=1)

        # queue2 should still receive the message
        self.assertEqual(queue2.get(), test_message)
        pubsub.unsubscribe(queue2)
