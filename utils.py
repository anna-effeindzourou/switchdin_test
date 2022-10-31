# Helper functions are stored here
import pika
from custom_exceptions import PublishError, BrokerConnectionError


def connect_broker(queue_name, username, password):
    # Establish connection to the broker and the queue
    try:
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
    except:
        raise BrokerConnectionError("failed to connect to broker")

    return connection, channel


def publish_to_queue(username, password, queue_name, data):
    # Send data to the queue
    try:
        connection, channel = connect_broker(queue_name, username, password)
        channel.basic_publish(exchange="", routing_key=queue_name, body=f"{data}")
        print(f" [x] Sent {data}")
        connection.close()
    except Exception as error:
        raise PublishError(f"failed to publish ({error})")
