#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# create queue
channel.queue_declare(queue='direct_queue',durable=True)

#create exchange
channel.exchange_declare(exchange='direct_exchange',
                         exchange_type='direct',durable=True)

#bind queue to exchange
channel.queue_bind(queue='direct_queue', exchange='direct_exchange', routing_key='tour.booked')

#publish message
channel.basic_publish(exchange='direct_exchange',routing_key='tour.booked',body='send by exchanges')

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


#consume message
channel.basic_consume(queue='direct_queue',on_message_callback=print_message)

channel.start_consuming()
channel.stop_consuming()
