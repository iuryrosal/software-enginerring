# Esse arquivo realiza a logica para o recebimento de informações em filas
import pika, sys, os

def connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()
    return connection, channel

def consume_queue(name_queue, callback):
    connection, channel = connect()
    channel.queue_declare(queue = name_queue) 
    channel.basic_consume(queue = name_queue, on_message_callback = callback, auto_ack = True)
    print(f' [*] Waiting {name_queue} for messages.')
    channel.start_consuming()
