#!/usr/bin/env python
# coding=utf-8
import pika
from pika.exchange_type import ExchangeType
def producer(i,ip):
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(ip, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    for i in range(0,i):
        channel.basic_publish(exchange='', routing_key='hello', body="hello {i}")
        print(i)
    connection.close()
producer(500000,'192.168.1.107')
