#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# create queue
channel.queue_declare(queue='fanout_queue', durable=True)

#create exchange
channel.exchange_declare(exchange='fanout_exchange',
                         exchange_type='fanout')

#bind queue to exchange
#fanout will ignore the routing key
channel.queue_bind(exchange='fanout_exchange', queue='fanout_queue', routing_key='')

#publish message
channel.basic_publish(exchange='fanout_exchange',routing_key='',body='send by exchanges')

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

#consume messge
channel.basic_consume(queue='fanout_queue',on_message_callback=print_message)

channel.start_consuming()
channel.close()
connection.close
