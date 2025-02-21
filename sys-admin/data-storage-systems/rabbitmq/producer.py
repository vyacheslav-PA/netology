#!/usr/bin/env python
# coding=utf-8
import pika
from pika.exchange_type import ExchangeType
def producer(i,ip):
    text = 'hello netology ' + str(i)
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(ip, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=text)
    connection.close()
