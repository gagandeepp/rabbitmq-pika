#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('gdeep', 'gdeep')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# create queue
channel.queue_declare(queue='dead_letter_queue', durable=True, exclusive=False,auto_delete=False)

#create exchange
channel.exchange_declare(exchange='DLX',
                         exchange_type='direct',durable=True)

#bind queue to exchange
#fanout will ignore the routing key
channel.queue_bind(exchange='DLX', queue='dead_letter_queue', routing_key='')

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame.basic_properties.headers['x-first-death-reason'])

#consume messge
channel.basic_consume(queue='dead_letter_queue',auto_ack=True,on_message_callback=print_message)

channel.start_consuming()
channel.close()
connection.close