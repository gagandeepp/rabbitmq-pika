#!/usr/bin/env python
import pika
import pika.spec
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# create queue
channel.queue_declare(queue='header_queue', durable=True)

#create exchange
channel.exchange_declare(exchange='header_exchange',
                         exchange_type='headers')

#bind queue to exchange
headers = {
    'authorisation': 'jwt',
    'claim': 'rabbitmq'
}
#fanout will ignore the routing key
channel.queue_bind(exchange='header_exchange', queue='header_queue', arguments=headers)

#publish message
props = pika.spec.BasicProperties()
props.headers = headers
props.user_id = 123

channel.basic_publish('header_exchange','',props, str.encode('header message'))

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame.headers)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

#consume messge
channel.basic_consume(queue='header_queue',on_message_callback=print_message)

channel.start_consuming()
channel.close()
connection.close