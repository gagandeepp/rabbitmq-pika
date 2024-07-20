#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# create queue
channel.queue_declare(queue='topic_queue',durable=True)

#create exchange
channel.exchange_declare(exchange='topic_exchange',
                         exchange_type='topic',durable=True)

#bind queue to exchange
channel.queue_bind(queue='topic_queue', exchange='topic_exchange', routing_key='tour.*')

#publish message
channel.basic_publish(exchange='topic_exchange',routing_key='tour.confirm',body='confirm booking')
channel.basic_publish(exchange='topic_exchange',routing_key='tour.book',body='booking booked')
channel.basic_publish(exchange='topic_exchange',routing_key='tour.cancel',body='cancel booking')

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame)
    print(method_frame)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


#consume message
channel.basic_consume(queue='topic_queue',on_message_callback=print_message)

channel.start_consuming()
# channel.stop_consuming()
