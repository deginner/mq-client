import os
import sys
import unittest
import time

from mq_client import AsyncMQPublisher, AsyncMQConsumer

EXCHANGE = 'test_exchange'
EXCHANGE_TYPE = 'direct'
CLIENT_BROKER_URL = "amqp://guest:guest@localhost:5672/%2F" # %2F is "/" encoded

result = []  # global result for amqp responses

def on_message(channel, method, header, body):
    global result
    # Acknowledge message receipt
    channel.basic_ack(method.delivery_tag)
    if 'terminate' in result:
        result.remove('terminate')
        channel.parent_client.stop()
    elif body == "":
        return
    else:
        result.append(body)

consumer = AsyncMQConsumer(CLIENT_BROKER_URL,
                           on_message=on_message,
                           exchange=EXCHANGE,
                           queue="test_queue")

class SendSimple(unittest.TestCase):

    def test_send_empty_order(self):
        global result
        result = []

        def producer(publisher):
            publisher.publish('order')
            publisher.publish('terminate')
            publisher.publish('')
            publisher._connection.close()
            try:
                publisher.stop()
            except Exception as e:
                pass

        self.publisher = AsyncMQPublisher(CLIENT_BROKER_URL,
                                          producer=producer,
                                          exchange=EXCHANGE,
                                          queue="test_queue")
        self.publisher.run()
        consumer.run()
        self.assertEqual(result[0], 'order')


    def test_send_multiple_orders(self):
        global result
        result = []

        def producer(publisher):
            publisher.publish('order0')
            publisher.publish('order1')
            publisher.publish('order2')
            publisher.publish('terminate')
            publisher.publish('')
            publisher._connection.close()
            try:
                publisher.stop()
            except Exception as e:
                pass

        self.publisher = AsyncMQPublisher(CLIENT_BROKER_URL,
                                          producer=producer,
                                          exchange=EXCHANGE,
                                          queue="test_queue")

        self.publisher.run()
        consumer.run()
        self.assertEqual(result[0], 'order0')
        self.assertEqual(result[1], 'order1')
        self.assertEqual(result[2], 'order2')


if __name__ == "__main__":
    unittest.main()

