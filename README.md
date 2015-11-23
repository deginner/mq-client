# Message Queue Client

A client for a [RabbitMQ](http://rabbitmq.com/) message queue server. This "client" is really a set of wrappers and helpers for the [pika](http://pika.readthedocs.org/) client library.

## Install

This package is in Pypi and can be installed using pip.

`pip install mq-client`

## Consumer Example

To create a consumer client, initialized an instance of `AsyncMQConsumer` with a custom `on_message` function defined. This function will be called every time the client receives a message.

```
from mq_client import AsyncMQConsumer

def on_message(channel, method, header, body):
    global terminate
    # Acknowledge message receipt
    channel.basic_ack(method.delivery_tag)
    print body

consumer = AsyncMQConsumer("amqp://guest:guest@localhost:5672/%2F",
                           on_message=on_message)
consumer.run()
```

## Publisher Example

To create a publisher client, initialized an instance of `AsyncMQPublisher` with a custom `producer` function defined. This function will be called in a loop until the client is stopped, and is expected to publish messages to the queue.

```
from mq_client import AsyncMQPublisher

def producer(publisher):
    publisher.publish("message goes here")

publisher = AsyncMQPublisher(args.url,
                             producer=producer)
publisher.run()
```

## Commands

This package comes with helper commands for easy debugging of your message queue.

##### mqlisten

This command is an example listener which will echo any messages it recieves.

```
$ mqlisten --help
usage: mqlisten [-h] [--url URL] [--exchange EXCHANGE]
                [--exchange-type EXCHANGE_TYPE] [--queue QUEUE]
                [--routing-key ROUTING_KEY]

optional arguments:
  -h, --help            show this help message and exit
  --url URL
  --exchange EXCHANGE
  --exchange-type EXCHANGE_TYPE
  --queue QUEUE
  --routing-key ROUTING_KEY
```

##### mqpublish

This command publishes a single message using the configuration specified.

```
$ mqpublish --help
usage: mqpublish [-h] [--url URL] [--exchange EXCHANGE]
                 [--exchange-type EXCHANGE_TYPE] [--queue QUEUE]
                 [--routing-key ROUTING_KEY]
                 message

positional arguments:
  message               the message to publish

optional arguments:
  -h, --help            show this help message and exit
  --url URL
  --exchange EXCHANGE
  --exchange-type EXCHANGE_TYPE
  --queue QUEUE
  --routing-key ROUTING_KEY
```
