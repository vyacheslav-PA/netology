#!/usr/bin/env python
# coding=utf-8
import pika
def consumer(ip):
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(ip, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
    # channel.basic_consume(callback, queue='hello', no_ack=True)
    channel.basic_consume( 'hello', callback, auto_ack=True)
    channel.start_consuming()
consumer('192.168.1.102')