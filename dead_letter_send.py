#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('gdeep', 'gdeep')
parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

args = {
    'x-dead-letter-exchange' : 'DLX'
}
channel.queue_declare(queue='hello',passive=True, durable=True,exclusive= False,arguments= args)

def print_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(method_frame.routing_key)
    print(body)
    print(header_frame.basic_properties.headers['x-first-death-reason'])
    channel.basic_reject(delivery_tag=method_frame.delivery_tag,reque=False)

channel.basic_consume('hello',print_message,auto_ack=False)

connection.close()